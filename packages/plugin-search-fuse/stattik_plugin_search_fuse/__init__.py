import asyncio
from aioreactive import AsyncAnonymousObserver

from stattik import blackboard

from .fuse import FuseIndexer

async def index(val):
    print(val.__class__)
    indexer = FuseIndexer()
    await indexer.index()

async def install(app, options):
    print('installed')
    #subscription = await blackboard.index.subscribe_async( AsyncAnonymousObserver(hello))
    subscription = await blackboard.subscribe('index', index)
