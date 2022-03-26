from loguru import logger

import stattik.database

from .repositories import repositories

def create_database():
    return stattik.database.create_database(repositories)
