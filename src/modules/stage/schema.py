from typing import List, Optional
from pydantic import BaseModel, Field

from modules.port.schema import PortSchema


class RemoteOrgSchema(BaseModel):
    login: str


class RemoteRepoSchema(BaseModel):
    name: str


class RemoteBranchSchema(BaseModel):
    name: str


class StagingModel(BaseModel):
    id: int
    org_name: str
    repo_name: str
    branch_name: str
    exposed_port: int
    git: str
    enable_tg_notifications: bool
    enable_webhooks: Optional[bool] = Field(default=False)
    webhook_id: Optional[str] = Field(default=None)
    enable_ssl: bool
    enable_websockets: bool
    websockets_path: Optional[str] = Field(default=None)

class StageModel(BaseModel):
    id: int
    nginx_path: str
    title: str
    url: str
    assigned_port: PortSchema
    directory: str
    status: str
    staging: StagingModel


class CreateStageModel(BaseModel):
    org_name: str
    repo_name: str
    branch_name: str
    exposed_port: int
    env: Optional[List[str]] = Field(default=[])

    enable_tg_notifications: bool
    enable_webhooks: bool
    enable_ssl: bool
    enable_websockets: bool
    websockets_path: str


class DeleteStageModel(BaseModel):
    id: int