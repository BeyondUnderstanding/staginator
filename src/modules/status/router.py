from fastapi import APIRouter, Depends
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db import get_session
from models import Staging, Stage
from modules.status.schema import CreateStageModel, LogStageModel
from src.modules.telegrammanager import manager

status_router = APIRouter(prefix='/status')

@status_router.patch('/')
def handle_status_change(data: CreateStageModel, session: Session = Depends(get_session)):
    stage = session.scalar(select(Stage).where(
        and_(
            Staging.org_name == data.org,
            Staging.repo_name == data.repo,
            Staging.branch_name == data.branch
        )
    ).join(Staging).limit(1))
    stage.status = data.status
    if data.status == 'run':
        manager.stage_build_finished(stage.title, stage.url)
    session.add(stage)
    session.commit()
    return JSONResponse(status_code=200, content='ok')



@status_router.post('/')
def handle_log(data: LogStageModel, session: Session = Depends(get_session)):
    stage = session.scalar(select(Stage).where(
        and_(
            Staging.org_name == data.org,
            Staging.repo_name == data.repo,
            Staging.branch_name == data.branch
        )
    ).join(Staging).limit(1))
    stage.status = 'error'
    manager.stage_build_failed(stage.title, data.message)
    session.add(stage)
    session.commit()
    return JSONResponse(status_code=200, content='ok')