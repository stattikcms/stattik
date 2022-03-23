import os
import errno
from pathlib import Path

from loguru import logger

from stattik.site import Site

def create_renderer():
    renderer = Renderer.produce()
    return renderer

class RenderContext:
    def __init__(self, renderer, page, url=None, path=None, paginator=None):
        self.renderer = renderer
        self.page = page
        self.url = url if url else page.url
        self.path = path if path else page.path
        self.body = ''
        self.paginator = paginator
        self.children = []

    def add_context(self, url, path):
        child = RenderContext(self.renderer, self.page, url, path, self.paginator)
        self.add_child(child)

    def add_child(self, child):
        self.children.append(child)

class Renderer:

    def __init__(self):
        pass

    _instance = None
    @classmethod
    @property
    def instance(self):
        if self._instance:
            return self._instance
        self._instance = self.produce()
        return self._instance

    @classmethod
    def produce(self):
        self._instance = self()
        return self._instance

    async def render(self):
        site = Site.instance
        db = site.database
        #await db.begin()

        pages = await db['Page'].all()

        for page in pages:
            await self.render_page(page)

        dst_path = Path("dist/css/components.css")

        try:
            os.remove(dst_path)
        except OSError:
            pass

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dst_path, "w") as myfile:
            for css in site.css_scopes:
                text = str(css)
                myfile.write(text)

        #await db.end_session()

    async def render_page(self, page, context=None):
        if not context:
            context = RenderContext(self, page)

        async def receive():
            logger.debug('receive')

        async def send(msg):
            if msg['type'] != 'http.response.body':
                #logger.debug(msg['type'])
                return
            context.body = f"<!DOCTYPE html>\n{msg['body'].decode('utf-8')}"
            self.write_context(context)

        await self.render_context(context, receive, send)
        
        for child in context.children:
            await self.render_page(page, child)

    async def render_context(self, context, receive, send):
        url = context.url
        #logger.debug(f'name:  {url.name}')
        s_url = str(url)
        if s_url != '/' and url.suffix == '':
            s_url = f'{s_url}/'

        #logger.debug(f'render_page:url:  {s_url}')
        scope = {
            "type": "http",
            "method": "GET",
            "path": s_url,
            "headers": {},
            "context": context
        }

        router = Site.instance.router

        await router(scope, receive, send)

    def write_context(self, context):
        body = context.body
        dst_path = 'dist' / context.path

        if not os.path.exists(os.path.dirname(dst_path)):
            try:
                os.makedirs(os.path.dirname(dst_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(dst_path, "w") as text_file:
            text_file.write(body)
