from loguru import logger

import stattik.database

from .builders import builders

def create_architect():
    return stattik.architect.create_architect(builders)
