import os, sys
import asyncio
from pathlib import Path
import importlib.util

from loguru import logger

from dotenv import load_dotenv
load_dotenv(Path(os.getcwd()) / '.env')

import toml

from . import blackboard
from .core.collection import Collection

aliases = {}
#TODO:  Need to start Typing!
#NOTE:  Ref can either be a str or a Path

def to_path(ref):
    path = None
    if isinstance(ref, str):
        path = Path(ref)
    else:
        path = ref

    if path.parts[0] in aliases:
        path = Path(aliases[path.parts[0]]).joinpath('/'.join(path.parts[1:len(path.parts)]))

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
    
    #instance = None

    def __init__(self):
        self.collections = []
        self.database = None
        self.architect = None
        self.renderer = None
        self.indexer = None
        self.css_scopes = []
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
        site.on_create()
        await site.begin()
        return site

    @property
    async def page_count(self):
        return await self.database['Page'].count()

    def add_css(self, css):
        self.css_scopes.append(css)

    def on_create(self):
        pass

    @classmethod
    async def load_site(self):
        #config = toml.load('stattik.toml')
        config = self.load_config()
        environment = config['environment']
        for key, val in environment.items():
            os.environ.setdefault(key, val)

        root_name = environment['STATTIK_ROOT_MODULE']
        print(root_name)
        sys.path.append(f"./{root_name}")
        module_name = environment['STATTIK_SETTINGS_MODULE']
        module = importlib.import_module(module_name)

        attrs = {}
        for key in dir(module):
            #print(key)
            if key.startswith('__'):
                continue
            attrs[key] = module.__dict__[key]

        #TODO: Should probably use more intelligent merging?
        attrs.update(config)

        super_class = Site
        SiteClass = type(module_name, (super_class,), attrs)
        site = SiteClass()

        self.load_resolve(attrs)
        await self.load_plugins(site, attrs)

        return site

    @classmethod
    def load_config(self):
        config = {}
        path = Path(os.getcwd(), 'stattik-config.py')
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location(
                "stattik_config", path
            )
            stattik_config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(stattik_config)
            for key in dir(stattik_config):
                if key.startswith('__'):
                    continue
                config[key] = stattik_config.__dict__[key]
        #logger.debug(f'load_config:config: {config}')

        return config

    @classmethod
    def load_resolve(self, config):
        if 'resolve' in config:
            resolve = config['resolve']
            if 'alias' in resolve:
                global aliases
                aliases = resolve['alias']

    def load_collections(self):
        _collections = self.config['collections']
        for _collection in _collections:
            collection = Collection()
            self.collections.append(collection)

    @classmethod
    async def load_plugins(self, site, config):
        plugins = config['plugins']
        for plugin in plugins:
            use = plugin['use']
            plugin_module = importlib.import_module(use)
            await plugin_module.install(site, plugin['options'])

    async def begin(self):
        await self.database.begin()

    async def build(self):
        await self.assemble()
        await self.index()
        await self.render()

    async def assemble(self):
        await self.database.drop_all()
        await self.architect.build_site()

    async def render(self):
        await self.renderer.render()

    async def index(self):
        #await self.indexer.index()
        await blackboard.publish('index', self)
