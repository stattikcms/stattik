from typing import Any, Optional
from datetime import UTC, datetime

from sqlalchemy import (
    ForeignKey,
    Integer,
    JSON,
    String,
    DateTime,
    Text,
    func,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stattik.database import Repository
from stattik.repositories import Model
from stattik.data import Data

import sqlalchemy.types as types
from pathlib import Path


class PathType(types.TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return None if value is None else str(value)

    def process_result_value(self, value, dialect):
        return None if value is None else Path(value)


def utcnow():
    # NOTE: Naive UTC, to compare with the naive datetimes frontmatter produces
    return datetime.now(UTC).replace(tzinfo=None)


class Page(Model):
    def __init__(self, data=None) -> None:
        self.inject(data or {})

    def inject(self, data):
        for key in data:
            setattr(self, key, data[key])

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Page.id"))
    type: Mapped[str] = mapped_column(String(50))
    data: Mapped[Optional[Any]] = mapped_column(JSON)

    src_path: Mapped[Optional[Path]] = mapped_column(PathType())
    src_url: Mapped[Optional[Path]] = mapped_column(PathType())
    path: Mapped[Optional[Path]] = mapped_column(PathType())
    url: Mapped[Optional[Path]] = mapped_column(PathType())

    title: Mapped[Optional[str]] = mapped_column(String)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True, default=utcnow)
    stars: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    menu: Mapped[Optional[Any]] = mapped_column(JSON)

    description: Mapped[Optional[str]] = mapped_column(String)
    cover: Mapped[Optional[str]] = mapped_column(String)
    slug: Mapped[Optional[str]] = mapped_column(String)

    content: Mapped[Optional[str]] = mapped_column(Text)

    parent: Mapped[Optional["Page"]] = relationship(
        "Page",
        lazy="joined",
        cascade="all",
        backref="children",
        remote_side="Page.id",
    )

    __mapper_args__ = {"polymorphic_identity": "Page", "polymorphic_on": "type"}


class PageInput(Data):
    type: str
    title: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    cover: Optional[str] = None
    slug: Optional[str] = None


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
        q = await session.execute(select(func.count()).select_from(self.Model))
        return q.scalar_one()

    async def slice(self, start, stop):
        session = self.Session()
        q = await session.execute(
            select(self.Model).order_by(self.Model.id).slice(start, stop)
        )
        return q.scalars().all()

    async def latest(self, start, stop):
        session = self.Session()
        q = await session.execute(
            select(self.Model).order_by(self.Model.date.desc()).slice(start, stop)
        )
        return q.scalars().all()

    async def find_by_src_url(self, src_url):
        session = self.Session()
        q = await session.execute(
            select(self.Model).where(self.Model.src_url == Path(src_url))
        )
        return q.scalars().first()

    async def find_by_url(self, url):
        session = self.Session()
        q = await session.execute(
            select(self.Model).where(self.Model.url == Path(url))
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
            "id": mapped_column(Integer, ForeignKey("Page.id"), primary_key=True),
            "__mapper_args__": {"polymorphic_identity": name},
        },
    )
    repo = type(f"{name}Repository", (base,), {"Model": Model})
    _page_types[name] = repo
    return repo
