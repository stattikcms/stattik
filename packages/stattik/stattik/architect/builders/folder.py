import os, sys

from loguru import logger

from copy import copy
from pathlib import Path

from stattik import data

from .builder import Builder
from .job import Job


class FolderBuilder(Builder):

    def get_builder(self, job):
        if job.src_path.suffix in self.builders:
            builder = self.builders[job.src_path.suffix](self)
        else:
            builder = None
        return builder

    async def build(self, job):
        root = job.src_path
        config = job.config
        #print("root --", root)

        index_path = root / '_index.md'
        if os.path.exists(index_path):
            parent = await self.build_page(Job(index_path, config))
            config['parent'] = parent

        for entry in os.scandir(root):
            if entry.is_dir():
                #print('==', entry.name)
                await self.build_folder(Job(Path(root) / entry.name, copy(config)))
                continue
            if entry.name == '_index.md':
                continue

            path = Path(root, entry.name)
            if path.suffix == '.yml':
                continue
            #print('page---', path)

            await self.build_page(Job(path, config))

    async def build_folder(self, job):
        root = job.src_path
        config = job.config
        #print("root --", root)

        config_path = Path(root, '_index.yml')
        if os.path.exists(config_path):
            config.update(data.load(config_path))

        if 'builder' in config:
            builder = self[config['builder']](self)
            if builder.is_deferred:
                print('deferred')
                return self.defer(builder, Job(root, config))
            else:
                return await builder.build(Job(root, config))
        else:
            await self.build(job)

    async def build_page(self, job):
        #print(job.__dict__)
        builder = self.get_builder(job)
        await builder.build(job)
