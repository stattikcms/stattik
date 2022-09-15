from loguru import logger

import starlette.routing as srouting
from starlette.responses import HTMLResponse

from .vue import Vue
from .view import build_view
from .database import Database
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
    params = route.request['path_params']
    context = route.request['context']
    page = context.page
    #logger.debug(f'render_route:page:  {page.__dict__}')
    props = { 'v_context': context, 'v_page': page, 'v_site': Site.instance, 'v_db': Database.instance}
    props.update(params)
    view = build_view(route.matched, props)
    vu = await view.create_vu()

    #logger.debug(f"render_route:vu:  {vu}")
    body = await vu.render()
    return HTMLResponse( body )

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

def create_router(routes):
    router = Router(routes)
    router.on_create()
    return router