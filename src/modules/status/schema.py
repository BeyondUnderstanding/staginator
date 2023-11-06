from pydantic import BaseModel


class CreateStageModel(BaseModel):
    org: str
    repo: str
    branch: str
    status: str