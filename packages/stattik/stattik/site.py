import os, sys
import asyncio
from pathlib import Path
import importlib.util

from loguru import logger

from dotenv import load_dotenv

load_dotenv(Path(os.getcwd()) / ".env")

from . import blackboard
from .core.collection import Collection
from .settings import Settings

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

    @classmethod
    @property
    def instance(self):
        if self._instance:
            return self._instance
        self._instance = asyncio.run(Site.produce())
        return self._instance

    # instance = None

    def __init__(self):
        self.collections = []
        self.database = None
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

    def create_task(self, awaitable):
        self.tasks.append(asyncio.create_task(awaitable))

    async def run_tasks(self):
        for task in self.tasks:
            await task

    @classmethod
    async def produce(self):
        # NOTE: Need to set _instance here or it causes infinite recursion
        self._instance = site = await self.load_site()
        site.on_create(site) # requires self as argument
        await site.begin()
        return site

    @property
    async def page_count(self):
        return await self.database["Page"].count()

    def add_css(self, css):
        self.css_scopes.append(css)

    def on_create(self):
        pass

    @classmethod
    async def load_site(self):
        settings = Settings.instance
        site = Site()
        for key, val in settings.items():
            site.__setattr__(key, val)

        self.load_resolve(settings)
        await self.load_plugins(site, settings)

        return site

    @classmethod
    def load_resolve(self, config):
        if "resolve" in config:
            resolve = config["resolve"]
            if "alias" in resolve:
                global aliases
                aliases = resolve["alias"]

    def load_collections(self):
        _collections = self.config["collections"]
        for _collection in _collections:
            collection = Collection()
            self.collections.append(collection)

    @classmethod
    async def load_plugins(self, site, config):
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
