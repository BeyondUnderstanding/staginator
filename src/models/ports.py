from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base


class Stage(Base):
    nginx_path: Mapped[str]
    title: Mapped[str]
    url: Mapped[str]
    port_id: Mapped[int] = mapped_column(ForeignKey('assignedport.id'))
    directory: Mapped[str]
    status: Mapped[str]
    staging_id: Mapped[int] = mapped_column(ForeignKey('staging.id'))

    assigned_port: Mapped['AssignedPort'] = relationship(back_populates='stage')
    staging: Mapped['Staging'] = relationship(back_populates='stage')


class AssignedPort(Base):
    port: Mapped[int]

    stage: Mapped['Stage'] = relationship(back_populates='assigned_port')


class Staging(Base):
    org_name: Mapped[str]
    repo_name: Mapped[str]
    branch_name: Mapped[str]
    exposed_port: Mapped[int]
    git: Mapped[str]

    enable_tg_notifications: Mapped[bool]
    enable_webhooks: Mapped[Optional[bool]] = mapped_column(default=False)
    webhook_id: Mapped[Optional[str]] = mapped_column(default=None)

    enable_ssl: Mapped[bool]
    enable_websockets: Mapped[bool]
    websockets_path: Mapped[Optional[str]] = mapped_column(default=None)

    stage: Mapped['Stage'] = relationship(back_populates='staging', cascade='all, delete')


class Config(Base):
    key: Mapped[str]
    value: Mapped[str]

