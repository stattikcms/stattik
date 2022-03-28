import os, re
from pathlib import Path

from loguru import logger

from stattik.markdown import Markdown
import stattik.frontmatter

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

import aiohttp

from stattik.architect.builders import FolderBuilder, MarkdownBuilder, Job

GH_TOKEN = os.getenv('GH_TOKEN')

class ProjectsBuilder(FolderBuilder):
    extension = 'Projects'
    async def build(self, job):
        root = job.src_path
        config = job.config
        #print(root)
        #print(config)

        await super().build(job)

        transport = AIOHTTPTransport(
            url="https://api.github.com/graphql",
            headers={'Authorization': f"token {GH_TOKEN}"}
        )

        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:

            query = gql(
                """
                query { 
                viewer {
                    repositories(privacy:PUBLIC first: 10) {
                        edges {
                        node {
                            url
                            resourcePath
                            defaultBranchRef {
                                name
                            }
                            name
                            nameWithOwner
                            homepageUrl
                            usesCustomOpenGraphImage
                            openGraphImageUrl
                            descriptionHTML
                            shortDescriptionHTML
                            stargazerCount
                        }
                    }
                    }
                }
                }
            """
            )

            result = await session.execute(query)
            #print(result)
            edges = result['viewer']['repositories']['edges']
            for edge in edges:
                _node = edge['node']
                _node['defaultBranchRef'] = _node['defaultBranchRef']['name']
                node = {}
                for key, value in _node.items():
                    #print(value)
                    node[snake(key)] = value
                #print(node)
                path = Path(root, node['name'])
                job = Job(path, config)
                job.inject(node, prefix='gh_')
                job.stars = job.gh_stargazer_count
                await self.build_page(job)

    def get_builder(self, job):
        builder = super().get_builder(job)
        if not builder:
            builder = ProjectBuilder(self)
        return builder

def snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class ProjectBuilder(MarkdownBuilder):
    extension = 'Project'

    # TODO:  Need to abstract the source.  More reuse
    async def build(self, job):
        job.title = job.gh_name
        job.description = job.gh_short_description_html
        if job.gh_uses_custom_open_graph_image:
            job.cover = job.gh_open_graph_image_url
        else:
            job.cover = 'https://i.imgur.com/HEZ2YhB.jpg'

        src_path = job.src_path

        stem = src_path.stem
        if stem == '_index':
            stem = 'index'
        suffix = 'html'

        parent_path = Path('/'.join(src_path.parts[1:-1]))
        path = parent_path / f'{stem}.{suffix}'
        #job.path = path
        job.path =  Path('/'.join([x for x in path.parts if x != '_index']))

        url = Path('/')
        
        if path.name == 'index.html':
            #url = url.joinpath(parent_path)
            url = parent_path
        else:
            #url = url.joinpath(path)
            url = path
            #print(url)

        job.src_url = Path('/') / url
        #job.url = url
        job.url = Path('/') / Path('/'.join([x for x in url.parts if x != '_index']))

        text = await self.load_text(job)
        matter = stattik.frontmatter.loads(text)

        #logger.debug(f'build_md:metadata:  {matter.metadata}')
        metadata = matter.metadata
        md = Markdown.instance.md
        html = md.convert(matter.content)
        metadata['toc'] = md.toc_tokens
        job.inject(metadata)
        if hasattr(job, 'menu'):
            self.build_menu(job)
        job.content = html

        await self.create_page(job)

    async def load_text(self, job):
        async with aiohttp.ClientSession() as session:

            url = f"https://raw.githubusercontent.com/{job.gh_name_with_owner}/{job.gh_default_branch_ref}/README.md"
            async with session.get(url) as resp:
                #data = await resp.json()
                text = await resp.text()
                return text
