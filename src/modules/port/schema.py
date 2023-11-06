from typing import Optional

from pydantic import BaseModel
# from src.modules.stage.schema import StageSchema


class PortSchema(BaseModel):
    id: int
    port: int


class CreatePortSchema(BaseModel):
    port: int

