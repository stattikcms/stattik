from asyncio import current_task

from loguru import logger

from ariadne import make_executable_schema, QueryType, MutationType, SubscriptionType

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session

from stattik.schema import Schema
from stattik.models import Model
from stattik.settings import Settings

from .utils import json_serializer

class Database(Schema):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = self
        self.engine = None
        self.query_type = QueryType()
        self.mutation_type = MutationType()
        self.subscription_type = SubscriptionType()

        self.child_map = {}

    def add_child(self, schema):
        # TODO:  Hacky
        self.child_map[schema.Model.__tablename__] = schema
        return super().add_child(schema)

    def __getitem__(self, key):
        return self.child_map[key]

    async def begin(self):
        self.url = Settings.get_singleton()["DATABASE_URL"]
        logger.debug(f"Creating engine with URL: {self.url}")
        self.engine = engine = create_async_engine(
            self.url,
            json_serializer=json_serializer
        )
        
        #await self.drop_all()
        engine = self.engine

        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)

        async_session_factory = sessionmaker(engine, class_= AsyncSession)
        Schema.Session = Session = async_scoped_session(async_session_factory, scopefunc=current_task)

        self.register()


    async def end(self):
        await self.end_session()

    async def end_session(self):
        await self.Session.commit()
        await self.Session.remove()

    async def drop_all(self):
        await self.begin()
        async with self.engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)

    def make_executable(self):
        return make_executable_schema(
            self.get_gql(),
            self.query_type,
            self.mutation_type,
            self.subscription_type
        )

    def discover(self):
        pass

def create_database(repositories) -> Database:
    db = Database.produce()
    for repo in repositories:
        # TODO: check for instance or class.  For now just class/callable
        repo(db)
    return db
