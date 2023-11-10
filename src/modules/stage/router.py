from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from agents import create_stage_execute, delete_stage_execute, rebuild_stage_execute
from src.modules.configmanager import ConfigManager
from models import Staging, AssignedPort, Stage
from src.db import get_session
from .github.router import github_repos
from .schema import CreateStageModel, DeleteStageModel, StageModel
from src.modules.githubmanager import github
from src.modules.telegrammanager import manager


stage = APIRouter(prefix='/stage')
stage.include_router(github_repos)

@stage.post('/create')
async def create_stage(data: CreateStageModel, session: Session = Depends(get_session)):
    port = session.scalar(select(AssignedPort).where(
        AssignedPort.stage == None
    ))

    if not port:
        return JSONResponse(status_code=433, content={'error': 'No available ports'})

    if session.scalar(select(Staging).where(and_(
        Staging.org_name == data.org_name,
        Staging.repo_name == data.repo_name,
        Staging.branch_name == data.branch_name
    )).limit(1)):
        return JSONResponse(status_code=432, content={'error': 'Staging already exist'})

    new_staging = Staging(**data.model_dump(exclude={'env': True}))
    git_repo = github.get_organization(data.org_name).get_repo(data.repo_name)
    new_staging.git = git_repo.clone_url
    # current_hooks = git_repo.get_hooks()
    try:
        if data.enable_webhooks:
            hook = git_repo.create_hook(
                name='web',
                config={
                'content_type': 'json',
                'insecure_ssl': 1,
                'url': 'http://staginator.msk.beyondedge.ru/api/webhooks/github'
            },
            events=[
                'push'
            ],
            active=True)
            new_staging.webhook_id = hook.id
    except Exception:
        pass
    if data.enable_ssl:
        ...
    if data.enable_websockets:
        ...

    session.add(new_staging)

    new_stage = Stage()
    new_stage.title = f'staginator-{data.repo_name}-{data.branch_name}'
    new_stage.nginx_path = f'/etc/nginx/sites-enabled/{new_stage.title}'
    new_stage.url = f'http://{data.branch_name}.{data.repo_name}.staginator.local'
    new_stage.assigned_port = port
    new_stage.directory = f'/etc/staginator/{data.repo_name}_{data.branch_name}'
    new_stage.status = 'prepare'
    new_stage.staging = new_staging
    session.add(new_stage)
    session.commit()
    session.refresh(new_staging)
    session.refresh(new_stage)

    create_stage_execute(new_stage.directory, data.org_name, data.repo_name, new_staging.git, data.branch_name, port.port, data.exposed_port, data.env)

    nginx_vars = ConfigManager().parse(stage_name=f'{new_staging.branch_name}.{new_staging.repo_name}',
                                     logs_path=f'/etc/nginx/logs',
                                     deploy_port=new_stage.assigned_port.port)
    ConfigManager().write_nginx_config(nginx_vars, new_stage.nginx_path)

    manager.stage_created(new_stage.title, new_stage.url, new_staging.exposed_port, new_stage.assigned_port.port)

    return JSONResponse(status_code=201, content={'message': 'Created', 'id': new_staging.id})

@stage.delete('/delete')
async def delete_stage(id: int, session: Session = Depends(get_session)):
    staging = session.get(Staging, id)
    if not staging:
        return JSONResponse(status_code=404, content={'message': 'Stage not found'})
    delete_stage_execute(staging.stage.directory, staging.repo_name, staging.branch_name, staging.stage.nginx_path)
    try:
        if staging.enable_webhooks:
            hook = github.get_organization(staging.org_name).get_repo(staging.repo_name).get_hook(int(staging.webhook_id))
            hook.delete()
    except Exception:
        pass


    manager.stage_delete(staging.stage.title, staging.stage.url)
    session.delete(staging)
    session.commit()
    return JSONResponse(status_code=200, content={'message': 'Deleted'})

@stage.post('/rebuild')
async def rebuild_stage(id: int, session: Session = Depends(get_session)):
    staging = session.get(Staging, id)
    if not staging:
        return JSONResponse(status_code=404, content={'message': 'Stage not found'})

    rebuild_stage_execute(staging.stage.directory,
                          staging.org_name,
                          staging.repo_name,
                          staging.branch_name,
                          staging.stage.assigned_port.port,
                          staging.exposed_port)

    manager.stage_rebuild_start(staging.stage.title)
    return JSONResponse(status_code=200, content={'message': 'Task created'})

@stage.get('/', response_model=List[StageModel])
async def get_stages(session: Session = Depends(get_session)):
    stages = session.scalars(select(Stage))
    return stages
