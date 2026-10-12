from pathlib import Path

from loguru import logger

from stattik.site import Site

from .builders import Job, FolderBuilder

def create_architect(builders):
    ar = Architect.produce(builders)
    return ar

class Architect(FolderBuilder):
    _instance = None
    @classmethod
    @property
    def instance(self):
        if self._instance:
            return self._instance
        self._instance = self.produce()
        return self._instance

    @classmethod
    def produce(self, builders):
        self._instance = self(builders)
        return self._instance

    def __init__(self, builders):
        super().__init__()
        self.deferred = []
        self.builders = {}
        for builder in builders:
            # TODO: check for instance or class.  For now just class/callable
            self.builders[builder.extension] = builder

        self.site = Site.instance
        self.db = self.site.database

    def defer(self, builder, job):
        self.deferred.append( (builder, job) )

    async def build_site(self):
        site = Site.instance
        db = site.database
        await db.begin()

        config = { "type": "Page", "db": self.db, "parent": None }

        await self.build(Job(Path('content'), config))

        while self.deferred:
            deferred = self.deferred
            self.deferred = []
            for builder, job in deferred:
                await builder.build(job)

        await db.end_session()
