from loguru import logger

import uvicorn

from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from ariadne.asgi import GraphQL

import stattik
from stattik.application import Stattik
from stattik.database import Database

def create_app():
    db = Database.produce()

    async def on_startup():
        await db.begin()

    async def on_shutdown():
        pass

    app = Stattik.produce(
        debug=True,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown]
    )
    schema = db.make_executable()

    app.mount("/graphql", GraphQL(schema, debug=True, introspection=True))
    app.mount('/', app=StaticFiles(directory='dist', html=True), name="public")

    return app

stattik.create_app = create_app

# WARNING:  You must pass the application as an import string to enable 'reload' or 'workers'.
def develop():
    uvicorn.run(
        'stattik:create_app',
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=["build"],
        reload_includes=["content"],
        log_level="info",
        factory=True
    )
