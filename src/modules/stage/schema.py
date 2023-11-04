from typing import List, Optional
from pydantic import BaseModel


class RemoteOrgSchema(BaseModel):
    login: str


class RemoteRepoSchema(BaseModel):
    name: str


class RemoteBranchSchema(BaseModel):
    name: str


class StageSchema(BaseModel):
    id: int
    title: str
    url: str
    port: int
    directory: str
    status: str
    repo_id: int

