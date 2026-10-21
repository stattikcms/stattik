from asyncio import current_task

from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session, async_sessionmaker

from stattik.schema import Schema
from stattik.repositories import Model
from stattik.settings import Settings

from .utils import json_serializer

class Database(Schema):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = self
        self.engine = None

        self.child_map = {}

    def __getitem__(self, key):
        return self.child_map[key]

    def add_child(self, schema):
        # TODO:  Hacky
        self.child_map[schema.Model.__tablename__] = schema
        return super().add_child(schema)

    async def begin(self, url=None):
        # NOTE: Idempotent.  One engine per process, released by close()
        if self.engine is not None:
            return
        self.url = url or Settings.get_singleton()["DATABASE_URL"]
        logger.debug(f"Creating engine with URL: {self.url}")
        self.engine = engine = create_async_engine(
            self.url,
            json_serializer=json_serializer
        )

        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)

        # NOTE: Pages are read after the architect commits, so don't expire them (that would trigger implicit IO)
        async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        Schema.Session = async_scoped_session(async_session_factory, scopefunc=current_task)

    async def end(self):
        await self.close()

    async def end_session(self):
        assert self.Session is not None
        await self.Session.commit()
        await self.Session.remove()

    async def close(self):
        if self.engine is None:
            return
        if self.Session is not None:
            await self.Session.remove()
        await self.engine.dispose()
        self.engine = None

    async def reset(self):
        """Drop and recreate every table."""
        await self.begin()
        assert self.engine is not None
        async with self.engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)
            await conn.run_sync(Model.metadata.create_all)

    def discover(self):
        pass

def create_database(repositories) -> Database:
    db = Database.produce()
    for repo in repositories:
        # TODO: check for instance or class.  For now just class/callable
        repo(db)
    return db
