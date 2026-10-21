from pathlib import Path

from loguru import logger

from stattik.site import Site

from .builders import Job, FolderBuilder

def create_architect(builders):
    ar = Architect(builders)
    return ar

class Architect(FolderBuilder):
    def __init__(self, builders):
        super().__init__()
        self.deferred = []
        self.builders = {}
        for builder in builders:
            # TODO: check for instance or class.  For now just class/callable
            self.builders[builder.extension] = builder

        self.site = Site.get_singleton_sync()
        self.db = self.site.database

    def defer(self, builder, job):
        self.deferred.append( (builder, job) )

    async def build_site(self):
        site = await Site.get_singleton()
        db = site.database

        config = { "type": "Page", "db": self.db, "parent": None }

        await self.build(Job(Path('content'), config))

        while self.deferred:
            deferred = self.deferred
            self.deferred = []
            for builder, job in deferred:
                await builder.build(job)

        await db.end_session()
