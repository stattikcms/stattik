import asyncio
import uvicorn

from loguru import logger

from starlette.staticfiles import StaticFiles
from ariadne.asgi import GraphQL

import stattik
from stattik.application import Stattik
from stattik.database import Database
from stattik.schema import Schema

class HelloSchema(Schema):
    """
    extend type Query {
        counter: Int!
    }
    extend type Mutation {
        setCounter(val: Int!): Int
    }
    extend type Subscription {
        counter: Int
    }
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.counter = 0

    @query("counter")
    async def counter_query(self, root, info):
        return self.counter

    @mutation("setCounter")
    def counter_mutation(self, root, info, val):
        logger.debug(f"set_counter:  {val}")
        self.counter = val
        return self.counter

    @subscription("counter")
    def counter_subscription(self, counter, info):
        logger.debug('counter')
        return counter

    @source("counter")
    async def counter_source(self, obj, info):
        logger.debug('generate_counter')
        count = 0
        while True:
            await asyncio.sleep(1)
            yield count
            count += 1

def create_app():
    db = Database.produce()
    schema = HelloSchema.produce(db)
    #print(schema.__dict__)
    #gql = inspect.getdoc(schema)
    gql = db.get_gql()
    print(gql)
    #xschema = root.make_executable()
    #print(xschema)
    #print(xschema.__dict__)

    async def on_startup():
        await db.begin()

    async def on_shutdown():
        pass

    app = Stattik.produce(
        debug=True,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown]
    )

    xschema = db.make_executable()

    app.mount("/graphql", GraphQL(xschema, debug=True, introspection=True))

    return app

stattik.create_app = create_app

def main():
    uvicorn.run('stattik:create_app', host="0.0.0.0", port=8000, reload=True, log_level="info", factory=True)
    # Production:
    # gunicorn example:app -w 4 -k uvicorn.workers.UvicornWorker
if __name__ == "__main__":
    main()
