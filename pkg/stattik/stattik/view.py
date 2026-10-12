from copy import copy

from loguru import logger

class View:
    def __init__(self, component, props={}, parent=None) -> None:
        self.component = component
        self.props = props
        self.parent = parent
        self.instance = None
        self.children = {}

    async def create_vu(self):
        if not self.instance:
            props = copy(self.props)
            props.update({'v_view': self })
            self.instance = await self.component.produce(props)
        return self.instance

def build_view(matched, props={}, name='default', ndx=0, parent=None):
    if ndx > len(matched) -1:
        return None

    record = matched[ndx]
    #logger.debug(f'build_view:record:  {record.__dict__}')

    if not name in record.components:
        return build_view(matched, props, name, ndx+1, parent)

    component = record.components[name]
    view = View(component, props, parent)
    view_names = component.views if hasattr(component, 'views') else []

    for rec_name in view_names:
        #logger.debug(f"view name: {rec_name}")
        for rec_ndx, rec in enumerate(matched, ndx+1):
            if rec_name in rec.components:
                #logger.debug(f'build_view:record:  {record.__dict__}')
                view.children[rec_name] = build_view(matched, props, rec_name, rec_ndx, view)
                break

    #logger.debug(f'build_view:view:  {view.__dict__}')
    return view

def print_view(view):
    print(view)
    print(view.__dict__)