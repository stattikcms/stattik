import os

import asyncio
import importlib
from pathlib import Path
from typing import Self

from loguru import logger

from dotenv import load_dotenv

load_dotenv(Path(os.getcwd()) / ".env")

from . import blackboard
from .settings import Settings
from .database import Database

aliases = {}
# TODO:  Need to start Typing!
# NOTE:  Ref can either be a str or a Path


def to_path(ref):
    path = None
    if isinstance(ref, str):
        path = Path(ref)
    else:
        path = ref

    if path.parts[0] in aliases:
        path = Path(aliases[path.parts[0]]).joinpath(
            "/".join(path.parts[1 : len(path.parts)])
        )

    return path


class SiteConfigNotFound(Exception):
    pass


class Site:
    _instance = None

    def __init__(self):
        self.collections = []
        self.settings: Settings | None = None
        self.database: Database | None = None
        self.architect = None
        self.renderer = None
        self.indexer = None
        self.baker = None

        self.css_scopes = []
        self.stylesheets = [
            "/css/bundle.css",
            "/css/components.css",
            #'/css/pygments.css',
        ]
        self.markdown_extensions = [
            "meta",
            "toc",
            "tables",
            "pymdownx.highlight",
            "pymdownx.emoji",
            "pymdownx.superfences",
        ]

        self.tasks = []

    @classmethod
    async def get_singleton(cls):
        if cls._instance is not None:
            return cls._instance
        cls._instance = site = await cls.load_site()
        site.on_create()
        hook = site.settings.get("on_create")
        if hook:
            hook(site)
        await site.begin()
        return site

    @classmethod
    def get_singleton_sync(cls):
        if cls._instance is not None:
            return cls._instance
        loop = asyncio.get_event_loop()
        return asyncio.run(cls.get_singleton())

    def create_task(self, awaitable):
        self.tasks.append(asyncio.create_task(awaitable))

    async def run_tasks(self):
        for task in self.tasks:
            await task

    @property
    async def page_count(self):
        return await self.database["Page"].count()

    def add_css(self, css):
        self.css_scopes.append(css)

    def on_create(self):
        from .repositories.page import PageRepository, define_page_type
        from .database import create_database
        from .routing import create_router
        from .architect import create_architect
        from .architect.builders import MarkdownBuilder
        from .renderer import create_renderer
        from .indexer.fuse import FuseIndexer
        from .baker import create_baker

        settings = self.settings
        repositories = [PageRepository] + [
            t if isinstance(t, type) else define_page_type(t)
            for t in settings.get("page_types", ["Landing", "Post"])
        ]
        self.database = create_database(repositories)
        self.router = create_router(settings["routes"])
        self.architect = create_architect(settings.get("builders", [MarkdownBuilder]))
        self.renderer = create_renderer()
        self.indexer = settings.get("indexer", FuseIndexer)()
        self.baker = create_baker()

    @classmethod
    async def load_site(cls) -> "Site":
        settings = Settings.get_singleton()
        logger.debug(f"Loaded settings: {settings}")
        site = Site()
        site.settings = settings
        for key, val in settings.items():
            if key == "on_create":
                continue
            site.__setattr__(key, val)

        cls.load_resolve(settings)
        await cls.load_plugins(site, settings)

        return site

    '''
    @classmethod
    async def load_site(cls):
        settings = Settings.get_singleton()
        logger.debug(f"Loaded settings: {settings}")
        site = Site()
        for key, val in settings.items():
            site.__setattr__(key, val)

        cls.load_resolve(settings)
        await cls.load_plugins(site, settings)

        database_url = settings["DATABASE_URL"]
        logger.debug(f"Database URL: {database_url}")
        site.database = Database(database_url)

        return site
    '''

    @classmethod
    def load_resolve(cls, config):
        if "resolve" in config:
            resolve = config["resolve"]
            if "alias" in resolve:
                global aliases
                aliases = resolve["alias"]

    @classmethod
    async def load_plugins(cls, site, config):
        if "plugins" not in config:
            return
        plugins = config["plugins"]
        for plugin in plugins:
            use = plugin["use"]
            plugin_module = importlib.import_module(use)
            await plugin_module.install(site, plugin["options"])

    async def begin(self):
        await self.database.begin()

    async def assemble(self):
        await self.database.drop_all()
        await self.architect.build_site()

    async def index(self):
        # await self.indexer.index()
        await blackboard.publish("index", self)

    async def render(self):
        await self.renderer.render()

    async def bake(self):
        await self.baker.bake()

    async def build(self):
        await self.assemble()
        await self.index()
        await self.render()
        await self.bake()
