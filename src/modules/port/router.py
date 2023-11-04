from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models import AssignedPort
from src.db import get_session
from .schema import PortSchema, CreatePortSchema
from src.modules.schema import IDReturnSchema


port = APIRouter(prefix='/port')


@port.get('/', description='Get all ports', response_model=List[PortSchema])
async def get_ports(session: Session = Depends(get_session)):
    ports = session.scalars(select(AssignedPort)).all()
    return ports


@port.post('/', description='Create new assignable port', response_model=IDReturnSchema, status_code=201)
def create_port(data: CreatePortSchema, session: Session = Depends(get_session)):
    new_port = AssignedPort(**data.model_dump())
    session.add(new_port)
    session.commit()
    session.refresh(new_port)
    return IDReturnSchema(id=new_port.id)


@port.delete('/', description='Delete port')
def delete_port(id: int, session: Session = Depends(get_session)):
    port_obj = session.get(AssignedPort, id)
    if not port_obj:
        return JSONResponse(status_code=404, content='Port not found')

    session.delete(port_obj)
    session.commit()
    return JSONResponse(status_code=200, content='Deleted')
