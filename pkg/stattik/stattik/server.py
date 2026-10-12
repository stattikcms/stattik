import os, sys
from pathlib import Path

from loguru import logger

from starlette.applications import Starlette

class Stattik(Starlette):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def produce(self, *args, **kwargs):
        instance = self(*args, **kwargs)
        instance.create()
        return instance

    def create(self):
        pass
