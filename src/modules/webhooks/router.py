from fastapi import APIRouter

from src.modules.webhooks.schema import PushSchema

webhooks = APIRouter(prefix='/webhook')


@webhooks.post('/github')
async def handle_github_webhook(data: PushSchema):
    ...