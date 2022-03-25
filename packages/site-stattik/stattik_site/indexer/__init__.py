from loguru import logger

from stattik.indexer.fuse import FuseIndexer

def create_indexer():
    return FuseIndexer()
