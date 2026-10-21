from typing import Annotated, Any, Optional
from datetime import UTC, date, datetime, time
from itertools import islice
from pathlib import Path

import msgspec
from loguru import logger

from grotto.ogm import Rel, Unindexed
from grotto.ogm.model import to_value

from stattik.database import Repository
from stattik.repositories import Model
from stattik.data import Data


def utcnow():
    # NOTE: Naive UTC, to compare with the naive datetimes frontmatter produces
    return datetime.now(UTC).replace(tzinfo=None)


class Page(Model):
    type: str = "Page"
    data: Optional[Any] = None

    src_path: Optional[Path] = None
    src_url: Optional[Path] = None
    path: Optional[Path] = None
    url: Optional[Path] = None

    title: Optional[str] = None
    date: Optional[datetime] = msgspec.field(default_factory=utcnow)
    stars: Optional[int] = None
    menu: Optional[Any] = None

    description: Optional[str] = None
    cover: Optional[str] = None
    slug: Optional[str] = None

    # NOTE: Bodies are never queried by value, so keep them out of the value index
    content: Annotated[Optional[str], Unindexed] = None

    parents = Rel("child_of", "Page")
    children = Rel("child_of", "Page", incoming=True)

    @property
    def parent(self):
        return next(iter(self.parents), None)


class PageInput(Data):
    type: str
    title: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    cover: Optional[str] = None
    slug: Optional[str] = None


# NOTE: Builder state that rides along in a job, never page data
_SKIP = {"db", "config", "parent"}


class PageRepository(Repository):
    Input = PageInput
    Model = Page

    @property
    def session(self):
        return self.db.session

    def build(self, data):
        """Make a Model from a job's data.  Declared fields become fields, other front matter goes in extras."""
        fields = {f.name for f in msgspec.structs.fields(self.Model)}
        kwargs = {}
        extras = {}
        for key, value in data.items():
            if key in _SKIP:
                continue
            if key in fields:
                kwargs[key] = value
                continue
            try:
                to_value(value)
            except TypeError:
                logger.debug(f"Not storing {key!r}: {type(value).__name__} can't be stored")
                continue
            extras[key] = value
        # NOTE: YAML reads a bare date as a date, which wouldn't sort against datetimes
        if type(kwargs.get("date")) is date:
            kwargs["date"] = datetime.combine(kwargs["date"], time())
        return self.Model(**kwargs, extras=extras)

    async def add(self, page, parent=None):
        self.session.add(page)
        if parent is not None:
            page.parents.add(parent)
        return page

    async def create(self, data):
        return await self.add(self.build(data), data.get("parent"))

    async def all(self):
        return list(self.session.find(self.Model))

    async def count(self):
        # NOTE: Count the label index directly, without loading every page
        return sum(1 for _ in self.session.graph.find(self.Model.__label__))

    async def slice(self, start, stop):
        return list(islice(self.session.find(self.Model), start, stop))

    async def latest(self, start, stop):
        pages = sorted(self.session.find(self.Model), key=lambda page: page.date or datetime.min, reverse=True)
        return pages[start:stop]

    async def find_by_src_url(self, src_url):
        return next(self.session.where(self.Model, "src_url", Path(src_url)), None)

    async def find_by_url(self, url):
        return next(self.session.where(self.Model, "url", Path(url)), None)


_page_types = {}


def define_page_type(name, base=PageRepository):
    """Create (or fetch) a Page subtype and its repository by name.  Its nodes carry both labels, so they are Pages too."""
    if name in _page_types:
        return _page_types[name]
    Model = type(name, (base.Model,), {})
    repo = type(f"{name}Repository", (base,), {"Model": Model})
    _page_types[name] = repo
    return repo
