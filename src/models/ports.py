from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base


class Stage(Base):
    nginx_path: Mapped[str]
    title: Mapped[str]
    url: Mapped[str]
    port_id: Mapped[int] = mapped_column(ForeignKey('hostport.id'))
    directory: Mapped[str]
    status: Mapped[str]
    staging_id: Mapped[int] = mapped_column(ForeignKey('staging.id'))

    assigned_port: Mapped['AssignedPort'] = relationship(back_populates='stage')
    staging: Mapped['Staging'] = relationship(back_populates='stages')


class AssignedPort(Base):
    port: Mapped[int]

    stage: Mapped['Stage'] = relationship(back_populates='assigned_port')


class Staging(Base):
    org_name: Mapped[str]
    repo_name: Mapped[str]
    branch_name: Mapped[str]
    exposed_port: Mapped[int]

    enable_tg_notifications: Mapped[bool]
    enable_ssl: Mapped[bool]
    enable_websockets: Mapped[bool]
    websockets_path: Mapped[str]

    stages: Mapped[List['Stage']] = relationship(back_populates='repo')


class Config(Base):
    key: Mapped[str]
    value: Mapped[str]

