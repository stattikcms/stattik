import os, sys
from pathlib import Path
import importlib.util
from collections import UserDict

from loguru import logger

from dotenv import load_dotenv

load_dotenv(Path(os.getcwd()) / ".env")

from .data import load


class SiteConfigNotFound(Exception):
    pass


class Settings(UserDict):
    _instance = None

    @classmethod
    def get_singleton(cls):
        if cls._instance is None:
            cls._instance = cls.produce()
        return cls._instance

    @classmethod
    def produce(cls):
        # NOTE: Need to set _instance here or it causes infinite recursion
        settings = cls.load_settings()
        return settings

    @classmethod
    def load_settings(cls):
        config = cls.load_config()
        environment = config["environment"]
        for key, val in environment.items():
            os.environ.setdefault(key, val)

        root_name = environment["STATTIK_ROOT_MODULE"]
        logger.debug(f"root_name: {root_name}")
        sys.path.append(f"./{root_name}")
        module_name = environment["STATTIK_SETTINGS_MODULE"]
        logger.debug(f"module_name: {module_name}")
        module = importlib.import_module(module_name)

        attrs = {}
        for key in dir(module):
            # print(key)
            if key.startswith("__"):
                continue
            attrs[key] = module.__dict__[key]

        # TODO: Should probably use more intelligent merging?
        attrs.update(config)

        settings = Settings(attrs)

        return settings

    @classmethod
    def load_config(cls):
        config = {}
        path = Path(os.getcwd(), "stattik.yml")
        if os.path.exists(path):
            config = load("stattik.yml")

        path = Path(os.getcwd(), "stattik-config.py")
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location("stattik_config", path)
            stattik_config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(stattik_config)
            for key in dir(stattik_config):
                if key.startswith("__"):
                    continue
                #logger.debug(key, stattik_config.__dict__[key])
                config[key] = stattik_config.__dict__[key]
        # logger.debug(f'load_config:config: {config}')

        return config
