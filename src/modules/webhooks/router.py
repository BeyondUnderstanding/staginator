from fastapi import APIRouter, Depends
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from agents import rebuild_stage_execute
from db import get_session
from models import Staging
from modules.telegrammanager import manager
from src.modules.webhooks.schema import PushSchema

webhooks = APIRouter(prefix='/webhooks')


@webhooks.post('/github')
async def handle_github_webhook(data: PushSchema, session: Session = Depends(get_session)):
    repo_name = data.repository.name
    org_name = data.organization.login
    branch_name = data.ref.replace('refs/heads/', '')

    stage = session.scalar(select(Staging).where(
        and_(
            Staging.org_name==org_name,
            Staging.repo_name==repo_name,
            Staging.branch_name==branch_name
        )
    ))
    if not stage:
        return 'Not found'

    rebuild_stage_execute(stage.stage.directory,
                          org_name,
                          repo_name,
                          branch_name,
                          stage.stage.assigned_port.port,
                          stage.exposed_port)
    manager.stage_rebuild_start(stage.stage.title)
