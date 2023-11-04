from fastapi import APIRouter
from .port.router import port
from .stage.router import stage
from .webhooks.router import webhooks

main_router = APIRouter(prefix='/api')
main_router.include_router(port)
main_router.include_router(stage)
main_router.include_router(webhooks)