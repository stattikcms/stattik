from loguru import logger

import stattik.routing

from .routes import routes

def create_router():
    return stattik.routing.create_router(routes)
