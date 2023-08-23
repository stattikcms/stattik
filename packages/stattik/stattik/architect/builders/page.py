from copy import copy
from pathlib import Path

from loguru import logger

#import frontmatter

from stattik.markdown import Markdown

import stattik.frontmatter

from .builder import Builder

class PageBuilder(Builder):

    async def create_page(self, job):
        db = job.db
        type = job.type
        repo = db[type]
        page = repo.Model(job.__dict__)

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
        #print('Path', path)
        #job.path = path
        job.path =  Path('/'.join([x for x in path.parts if x != '_index']))
        #print('Job Path', job.path)
        
        if path.name == 'index.html':
            url = parent_path
        else:
            url = path
        #print(url)
        
        job.src_url = Path('/') / url
        #print(job.src_url)
        job.url = Path('/') / Path('/'.join([x for x in url.parts if x != '_index']))
        #print('Job url', job.url)

        logger.debug(f'Src Path: {src_path}')
        with open(src_path) as f:
            matter = stattik.frontmatter.load(f)

        #logger.debug(f'build_md:metadata:  {matter.metadata}')
        metadata = matter.metadata
        md = Markdown.instance.md
        html = md.convert(matter.content)
        '''
        toc_tokens = md.toc_tokens
        print(toc_tokens)
        metadata['toc'] = toc_tokens
        '''
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
            item_path = Path(job.src_path.parent) / f"{item['url']}.md"
            if item_path.is_file():
                #print('File:  ', item_path)
                item['url'] = "/" / Path('/'.join(job.path.parts[0:-1])) / f"{item['url']}.html"
            else:
                #print('Dir:  ', item_path)
                item['url'] = "/" / Path('/'.join(job.path.parts[0:-1])) / item['url']

            new_menu.append(item)

        job.menu = new_menu
        #print(job.menu)

    def paginate(self, job):
        print(job.__dict__)
        #exit()