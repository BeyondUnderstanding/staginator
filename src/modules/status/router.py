from fastapi import APIRouter
from src.modules.githubmanager import github

status_router = APIRouter(prefix='/status')

