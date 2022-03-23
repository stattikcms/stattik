import os, sys
from pathlib import Path
import importlib.util

from loguru import logger

from starlette.applications import Starlette

class Stattik(Starlette):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        #self.config = {}

    @classmethod
    def produce(self, *args, **kwargs):
        instance = self(*args, **kwargs)
        instance.create()
        return instance

    def create(self):
        pass
        #self.config = self.load_config()
        #self.plugins = self.load_plugins()

    '''
    def load_config(self):
        config = self.config
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
        logger.debug(f'load_config:config: {config}')
        return config
            
    '''