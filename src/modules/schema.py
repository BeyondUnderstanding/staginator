from pydantic import BaseModel


class IDReturnSchema(BaseModel):
    id: int