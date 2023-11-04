from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from src.db import get_session
from src.modules.schema import IDReturnSchema
from .github.router import github_repos


stage = APIRouter(prefix='/stage')
stage.include_router(github_repos)


