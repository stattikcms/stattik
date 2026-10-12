from loguru import logger

from .applications import Stattik

def dev():
    logger.debug('dev')

def build():
    logger.debug('build')
    app = Stattik.produce()