from loguru import logger

import starlette.routing as srouting
from starlette.responses import HTMLResponse, PlainTextResponse

from .vue import Vue
from .view import build_view
from .site import Site


class RouteRecord:
    def __init__(self, data={}, parent=None) -> None:
        self.parent = parent
        self.children = []
        self.components = {}
        self.inject(data)

    def inject(self, data):
        for key in data:
            setattr(self, key, data[key])

    @property
    def component(self):
        return self.components['default']

    @component.setter
    def component(self, value):
        self.components['default'] = Vue.resolve(value)

def build_records(items, parent=None):
    records = []
    for item in items:
        records.append(build_record(item, parent))
    return records

def build_record(item, parent):
    record = RouteRecord(item, parent)
    if 'children' in item:
        record.children = build_records(item['children'], record)
    return record

def print_records(records):
    for record in records:
        #logger.debug(f'record:  {record.__dict__}')
        print_records(record.children)

def print_matched(records):
    for record in records:
        logger.debug(f'record:  {record.__dict__}')

class Route:
    def __init__(self, request, matched) -> None:
        self.request = request
        self.matched = matched

def fix_path(path):
    if path == '/':
        return path
    return f"/{path}"

async def render_route(route):
    #logger.debug(f'render_route:route:  {route.__dict__}')
    #logger.debug(f'render_route:request:  {route.request.__dict__}')
    #matched = route.matched
    #print_matched(matched)
    #page = route.request['page']
    context = route.request.scope.get('context')
    if context is not None:
        return HTMLResponse(await render_context(route, context))

    # NOTE: No context means a live request from the dev server, so look up the page ourselves
    context = await lookup_context(route.request)
    if context is None:
        return PlainTextResponse("Not Found", status_code=404)
    return HTMLResponse(f"<!DOCTYPE html>\n{await render_context(route, context)}")

async def render_context(route, context):
    params = route.request['path_params']
    page = context.page
    #logger.debug(f'render_route:page:  {page.__dict__}')
    site = await Site.get_singleton()
    props = { 'v_context': context, 'v_page': page, 'v_site': site, 'v_db': site.database}
    props.update(params)
    view = build_view(route.matched, props)
    vu = await view.create_vu()

    #logger.debug(f"render_route:vu:  {vu}")
    return await vu.render()

def route_path(url):
    """Format a page url the way the routes expect it:  folders get a trailing slash."""
    s_url = str(url)
    if s_url != '/' and url.suffix == '':
        s_url = f'{s_url}/'
    return s_url

def split_page_suffix(path):
    """Split '/blog/page/2' into ('/blog', ['page', '2']).  Paginated urls render from the listing page itself."""
    parts = [part for part in path.split('/') if part]
    suffix = []
    if len(parts) >= 2 and parts[-2] == 'page' and parts[-1].isdigit():
        parts, suffix = parts[:-2], parts[-2:]
    return '/' + '/'.join(parts), suffix

async def resolve_path(path):
    """
    Map a public request path to the source path the routes are written against.
    NOTE: Folders like _index group pages without appearing in the public url, so '/post.html' may live at '/_index/post.html'
    """
    base, suffix = split_page_suffix(path)
    site = await Site.get_singleton()
    repo = site.database['Page']
    page = await repo.find_by_src_url(base) or await repo.find_by_url(base)
    if page is None:
        return path
    if not suffix:
        return route_path(page.src_url)
    return route_path(page.src_url.joinpath(*suffix))

async def lookup_context(request):
    from .renderer import RenderContext

    src_url, _ = split_page_suffix(request.url.path)

    site = await Site.get_singleton()
    page = await site.database['Page'].find_by_src_url(src_url)
    if page is None:
        return None
    return RenderContext(site.renderer, page)

def print_routes(routes):
    for route in routes:
        logger.debug(f'route:  {route.__dict__}')
        if isinstance(route, srouting.Mount):
            print_routes(route.routes)

class Router:
    def __init__(self, routes):
        self.routes = routes

    async def __call__(self, scope, receive, send) -> None:
        return await self.router(scope, receive, send)

    def on_create(self):
        self.app_record = RouteRecord()
        self.app_record.component = Vue.create_app("src/App")

        records = build_records(self.routes)

        self.sroutes=self.build_routes(records)
        #print_routes(self.sroutes)

        self.router = srouting.Router(routes=self.sroutes)

    def build_routes(self, records):
        routes = []
        for record in records:
            routes.append(self.build_route(record))
        return routes

    def build_route(self, record):
        if len(record.children) != 0:
            routes = []
            for child in record.children:
                routes.append(self.build_route(child))

            return srouting.Mount(fix_path(record.path), routes=routes)

        matched = self.build_matched(record)
        async def wrapper(request):
            return await render_route(Route(request, matched))
        return srouting.Route(fix_path(record.path), wrapper)

    def build_matched(self, record):
        #logger.debug(f'build_matched:record:  {record.__dict__}')
        if not record.parent:
            return [self.app_record, record]
        result = self.build_matched(record.parent)
        result.append(record)
        return result

    @classmethod
    def produce(cls, routes) -> "Router":
        router = Router(routes)
        router.on_create()
        return router
    
def create_router(routes):
    router = Router(routes)
    router.on_create()
    return router
