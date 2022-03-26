import asyncio
from aioreactive import AsyncAnonymousObserver

from stattik import blackboard

from .fuse import FuseIndexer

async def index(val):
    indexer = FuseIndexer()
    await indexer.index()

async def install(app, options):
    subscription = await blackboard.subscribe('index', index)
