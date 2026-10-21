import os
from pathlib import Path

from loguru import logger

import uvicorn

from contextlib import asynccontextmanager
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.staticfiles import StaticFiles

from stattik.server import Stattik
from stattik.site import Site


class DevApp:
    """Serves assets from dist and renders everything else live through the site router."""

    def __init__(self):
        self.static = StaticFiles(directory="dist", check_dir=False)

    async def __call__(self, scope, receive, send):
        site = await Site.get_singleton()
        if scope["type"] != "http":
            return await site.router(scope, receive, send)

        path = scope["path"]
        if path == "/css/components.css":
            css = "".join(str(css) for css in site.css_scopes)
            response = Response(css, media_type="text/css")
            return await response(scope, receive, send)

        suffix = Path(path).suffix
        if suffix and suffix != ".html" and Path("dist", path.lstrip("/")).is_file():
            return await self.static(scope, receive, send)

        await site.router(scope, receive, send)


@asynccontextmanager
async def lifespan(app: Starlette):
    # Rebuild the database and search index so every start reflects the current content
    site = await Site.get_singleton()
    await site.assemble()
    await site.index()
    app.mount("/", app=DevApp())
    yield


def create_app():
    app = Stattik.produce(debug=True, lifespan=lifespan)
    return app


# WARNING:  You must pass the application as an import string to enable 'reload' or 'workers'.
def develop():
    uvicorn.run(
        "stattik.management.develop:create_app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        factory=True,
        reload=True,
        reload_includes=["*.md", "*.yml", "*.vue", "*.py"],
        reload_excludes=output_dirs(),
    )


def output_dirs():
    # NOTE: The build writes compiled .vue files to build/ and assets to dist/, which would loop the reloader.
    # uvicorn only treats an exclude as a directory if it exists, and compares absolute paths.
    dirs = []
    for name in ("build", "dist", "node_modules"):
        path = Path(os.getcwd(), name)
        if name != "node_modules":
            path.mkdir(exist_ok=True)
        if path.is_dir():
            dirs.append(str(path))
    return dirs
