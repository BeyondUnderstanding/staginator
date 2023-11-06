from typing import List, Optional
from pydantic import BaseModel, Field


class RemoteOrgSchema(BaseModel):
    login: str


class RemoteRepoSchema(BaseModel):
    name: str


class RemoteBranchSchema(BaseModel):
    name: str



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