from typing import Optional
from datetime import datetime
import json

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    JSON,
    String,
    DateTime,
    Text,
    event,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy.future import select

from stattik.database import Repository
from stattik.repositories import Model
from stattik.data import Data

import sqlalchemy.types as types
from pathlib import Path


class PathType(types.TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return Path(value)


class Page(Model):
    def __init__(self, data={}) -> None:
        self.inject(data)

    def inject(self, data):
        for key in data:
            setattr(self, key, data[key])

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("Page.id"))
    type = Column(String(50))
    data = Column(JSON)

    src_path = Column(PathType())
    src_url = Column(PathType())
    path = Column(PathType())
    url = Column(PathType())

    title = Column(String(50))
    date = Column(DateTime, index=True, default=datetime.utcnow())
    stars = Column(Integer, index=True)
    menu = Column(JSON)

    description = Column(String(50))
    cover = Column(String(50))
    slug = Column(String(50))

    content = Column(Text)

    parent = relationship(
        "Page",
        lazy="joined",
        cascade="all",
        backref="children",
        remote_side="Page.id",
    )

    __mapper_args__ = {"polymorphic_identity": "Page", "polymorphic_on": type}


class PageInput(Data):
    type: str
    title: Optional[str]
    date: Optional[datetime]
    description: Optional[str]
    cover: Optional[str]
    slug: Optional[str]


class PageRepository(Repository):
    Input = PageInput
    Model = Page

    async def add(self, page):
        session = self.Session()
        session.add(page)
        await session.flush()

    async def create(self, data):
        session = self.Session()
        page = self.Model(**dict(data))
        session.add(page)
        await session.flush()

    async def all(self):
        session = self.Session()
        q = await session.execute(select(self.Model).order_by(self.Model.id))
        return q.scalars().all()

    async def count(self):
        session = self.Session()
        q = await session.execute(
            select(func.count()).select_from(select(self.Model).subquery())
        )
        count = q.scalars().one()
        return count

    async def child_count(self):
        session = self.Session()
        q = await session.execute(
            select(func.count()).select_from(select(self.Model.children).subquery())
        )
        count = q.scalars().one()
        return count

    async def slice(self, start, stop):
        session = self.Session()
        q = await session.execute(
            select(self.Model).order_by(self.Model.id).slice(start, stop)
        )
        return q.scalars().all()

    async def latest(self, start, stop):
        session = self.Session()
        q = await session.execute(
            select(self.Model).order_by(self.Model.date).slice(start, stop)
        )
        return q.scalars().all()

    async def find_by_src_url(self, src_url):
        session = self.Session()
        q = await session.execute(
            select(self.Model).where(self.Model.src_url == Path(src_url))
        )
        return q.scalars().first()


_page_types = {}


def define_page_type(name, base=PageRepository):
    """Create (or fetch) a polymorphic Page subtype and its repository by name."""
    if name in _page_types:
        return _page_types[name]
    Model = type(
        name,
        (base.Model,),
        {
            "id": Column(Integer, ForeignKey("Page.id"), primary_key=True),
            "__mapper_args__": {"polymorphic_identity": name},
        },
    )
    repo = type(f"{name}Repository", (base,), {"Model": Model})
    _page_types[name] = repo
    return repo
