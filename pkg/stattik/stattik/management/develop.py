import asyncio

from loguru import logger

import uvicorn

from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from stattik.server import Stattik
from stattik.database import Database
from stattik.site import Site

site = None

async def create_site():
    global site
    site = await Site.produce()
    await site.begin()

def create_app():

    async def on_startup():
        pass

    async def on_shutdown():
        pass

    app = Stattik.produce(
        debug=True,
        routes=site.router.sroutes,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown]
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
