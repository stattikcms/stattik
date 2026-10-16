import os, sys
from pathlib import Path

from loguru import logger

from starlette.applications import Starlette

class Stattik(Starlette):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def produce(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        instance.create()
        return instance

    def create(self):
        pass
