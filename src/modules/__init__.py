from fastapi import APIRouter
from .port.router import port
from .stage.router import stage
from .webhooks.router import webhooks
from .status.router import status_router

main_router = APIRouter(prefix='/api')
main_router.include_router(port)
main_router.include_router(stage)
main_router.include_router(webhooks)
main_router.include_router(status_router)