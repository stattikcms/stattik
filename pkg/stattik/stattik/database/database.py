from loguru import logger

from grotto.core import Batch, Graph, MemoryKV, SQLiteKV
from grotto.ogm import Session

from stattik.schema import Schema
from stattik.repositories import SCHEMA
from stattik.settings import Settings


def open_kv(url):
    """
    Open the grotto store a DATABASE_URL names:  memory:// or sqlite:///path/to/file.db
    NOTE: sqlite+aiosqlite:/// is accepted too, so settings from the SQLAlchemy days keep working
    """
    scheme, sep, rest = url.partition("://")
    if not sep:
        raise ValueError(f"Not a database URL: {url!r}")
    if scheme == "memory":
        return MemoryKV()
    if scheme in ("sqlite", "sqlite+aiosqlite"):
        # NOTE: sqlite:///./stattik.db is relative, sqlite:////abs/stattik.db is absolute
        return SQLiteKV(rest.removeprefix("/") or ":memory:")
    raise ValueError(f"Unsupported database URL: {url!r}")


class Database(Schema):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = self
        self.kv = None
        self.graph = None
        self.session = None

        self.child_map = {}

    def __getitem__(self, key):
        return self.child_map[key]

    def add_child(self, schema):
        self.child_map[schema.Model.__label__] = schema
        return super().add_child(schema)

    async def begin(self, url=None):
        # NOTE: Idempotent.  One store and one session per process, released by close()
        if self.kv is not None:
            return
        self.url = url or Settings.get_singleton()["DATABASE_URL"]
        logger.debug(f"Opening store with URL: {self.url}")
        self.kv = open_kv(self.url)
        self.graph = Graph(self.kv)
        # NOTE: Pages stay usable after commit, so the architect's pages can be read by the renderer
        self.session = Session(self.graph, SCHEMA)

    async def end(self):
        await self.close()

    async def end_session(self):
        assert self.session is not None
        self.session.commit()

    async def close(self):
        if self.kv is None:
            return
        self.session.rollback()
        self.kv.close()
        self.kv = None
        self.graph = None
        self.session = None

    async def reset(self):
        """Delete everything in the store."""
        await self.begin()
        assert self.kv is not None
        self.session.rollback()
        batch = Batch()
        for name in self.kv.keyspaces():
            space = self.kv.keyspace(name)
            for key, _ in self.kv.scan(space):
                batch.delete(space, key)
        self.kv.write(batch)
        self.session = Session(self.graph, SCHEMA)

    def discover(self):
        pass

def create_database(repositories) -> Database:
    db = Database.produce()
    for repo in repositories:
        # TODO: check for instance or class.  For now just class/callable
        repo(db)
    return db
