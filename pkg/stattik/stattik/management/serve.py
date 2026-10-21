from contextlib import asynccontextmanager

from loguru import logger

import uvicorn

from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette

from stattik.site import Site
from stattik.server import Stattik


@asynccontextmanager
async def lifespan(app: Starlette):
    # Code to run on startup
    print("Startup")
    site = await Site.get_singleton()
    db = site.database
    app.mount("/", app=StaticFiles(directory="dist", html=True), name="public")

    yield
    # Code to run on shutdown
    print("Shutdown")
    await site.end()


def create_app():
    app = Stattik.produce(lifespan=lifespan)

    return app


# WARNING:  You must pass the application as an import string to enable 'reload' or 'workers'.
def serve():
    uvicorn.run(
        "stattik.management.serve:create_app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        factory=True,
    )
