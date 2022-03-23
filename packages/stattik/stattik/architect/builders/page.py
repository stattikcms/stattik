from copy import copy
from pathlib import Path

from loguru import logger

#import frontmatter

from stattik.markdown import md

import stattik.frontmatter

from .builder import Builder

class PageBuilder(Builder):

    async def create_page(self, job):
        db = job.db
        type = job.type
        repo = db[type]
        page = repo.Model(job.__dict__)

        #type = page.type
        #repo = self.architect.db[type]

        await repo.add(page)


class MarkdownBuilder(PageBuilder):
    extension = '.md'

    async def build(self, job):
        src_path = job.src_path

        stem = src_path.stem
        if stem == '_index':
            stem = 'index'
        suffix = 'html'

        parent_path = Path('/'.join(src_path.parts[1:-1]))
        path = parent_path / f'{stem}.{suffix}'
        job.path = path

        url = Path('/')
        
        if path.name == 'index.html':
            url = url.joinpath(parent_path)
        else:
            url = url.joinpath(path)
        
        job.url = url

        with open(src_path) as f:
            matter = stattik.frontmatter.load(f)

        #logger.debug(f'build_md:metadata:  {matter.metadata}')
        metadata = matter.metadata
        html = md.convert(matter.content)
        metadata['toc'] = md.toc_tokens
        job.inject(metadata)
        if hasattr(job, 'menu'):
            self.build_menu(job)
        #print(job.__dict__)
        job.content = html
        if hasattr(job, 'paginate'):
            self.paginate(job)

        await self.create_page(job)

    def build_menu(self, job):
        #print(job.menu)
        new_menu = []
        for item in job.menu:
            src_path = job.src_path
            item_path = Path(src_path.parent) / f"{item['url']}.md"
            if item_path.is_file():
                item['url'] = "/" / Path('/'.join(src_path.parts[1:-1])) / f"{item['url']}.html"
            else:
                item['url'] = "/" / Path('/'.join(src_path.parts[1:-1])) / item['url']
            new_menu.append(item)

        job.menu = new_menu
        #print(job.menu)

    def paginate(self, job):
        print(job.__dict__)
        #exit()