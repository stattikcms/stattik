import asyncio

from loguru import logger

import uvicorn

from contextlib import asynccontextmanager
from starlette.applications import Starlette

from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from stattik.server import Stattik
from stattik.database import Database
from stattik.site import Site

site = None

@asynccontextmanager
async def lifespan(app: Starlette):
    # Code to run on startup
    print("Startup")
    yield
    # Code to run on shutdown
    print("Shutdown")

async def create_site():
    global site
    site = await Site.get_singleton()

def create_app():

    app = Stattik.produce(
        debug=True,
        routes=site.router.sroutes,
        lifespan=lifespan
    )
    return app

async def _develop():
    await create_site()    
    #print(site)

    config = uvicorn.Config(
        'stattik.management.develop:create_app',
        host="0.0.0.0",
        port=8000,
        #reload=True,
        #reload_excludes=["build"],
        #reload_includes=["content"],
        log_level="info",
        factory=True
    )

    server = uvicorn.Server(config)
    await server.serve()

def develop():
    asyncio.run(_develop())
