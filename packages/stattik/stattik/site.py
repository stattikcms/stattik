import os, sys
from pathlib import Path
import importlib.util

from loguru import logger

from dotenv import load_dotenv
load_dotenv(Path(os.getcwd()) / '.env')

import toml

from .core.collection import Collection

aliases = {}
#TODO:  Need to start Typing!
#NOTE:  Ref can either be a str or a Path

def to_path(ref):
    path = None
    if isinstance(ref, str):
        #return Path(os.getcwd(), ref)
        path = Path(ref)
    else:
        path = ref

    #index = path.parts.index('ghi')
    #new_path = Path('/jkl/mno').joinpath(*path.parts[index:])
    if path.parts[0] in aliases:
        #print(path.parts[1:len(path.parts)])
        #exit()
        #path = Path(aliases[path.parts[0]]).joinpath(path.parts[1:-1])
        path = Path(aliases[path.parts[0]]).joinpath('/'.join(path.parts[1:len(path.parts)]))
        #print(path)
        #exit()

    #exit()
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
        self._instance = self._produce()
        return self._instance

    def __init__(self):
        self.collections = []
        self.database = None
        self.architect = None
        self.renderer = None
        self.indexer = None
        self.css_scopes = []

    @classmethod
    def _produce(self):
        # NOTE: Need to set _instance here or it causes infinite recursion
        self._instance = site = self.load_site()
        site.on_create()
        return site

    @property
    async def page_count(self):
        return await self.database['Page'].count()

    def add_css(self, css):
        self.css_scopes.append(css)

    def on_create(self):
        pass

    @classmethod
    def load_site(self):
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

        '''
        path = Path(os.getcwd(), 'src/settings.py')
        if not os.path.exists(path):
            raise SiteConfigNotFound()

        module_name = "stattik_site"
        spec = importlib.util.spec_from_file_location(
            module_name, path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        '''

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

        self.load_resolve(config)

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

    def load_plugins(self):
        plugins = self.config['plugins']
        for plugin in plugins:
            use = plugin['use']
            plugin_module = importlib.import_module(use)
            plugin_module.install(self, plugin['options'])

    async def begin(self):
        await self.database.begin()

    async def build(self):
        await self.begin()
        await self.database.drop_all()
        await self.architect.build_site()

    async def render(self):
        await self.begin()
        await self.renderer.render()

    async def index(self):
        await self.begin()
        await self.indexer.index()
