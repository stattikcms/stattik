import sys, os
import importlib
from copy import copy
from pathlib import Path

from .sfc.compiler import Compiler

from .site import to_path

class Vue:
    name = ''
    component_cache = {}
    global_components = {}
    def __init__(self, props={}) -> None:
        self.props = props
        self.inject(props)
        self.inject(self.data())
        self.registered_components = {}
        if hasattr(self, 'components'):
            for key, value in self.components.items():
                self.component(key, value)

    @classmethod
    async def produce(self, props):
        vu = self(props)
        context = props['v_context']
        paginator = context.paginator
        if not paginator:
            paginator = await vu.paginate()
        else:
            vu.paginator = paginator
        context.paginator = paginator
        #print(paginator)
        await vu.created()
        #print(vu.__dict__)
        return vu

    def component(self, name, klass):
        self.registered_components[name] = klass

    def inject(self, data):
        for key in data:
            setattr(self, key, data[key])

    # Overridables

    async def created(self):
        pass

    async def render(self, slots=None):
        return ''

    async def paginate(self, paginator=None):
        if hasattr(self, 'paginator'):
            return self.paginator
        if not paginator:
            return None
        self.paginator = paginator
        context = self.v_context
        context.paginator = paginator
        for page in paginator.pages:
            if page.number != 1:
                #context.add_context(page.url, page.path)
                context.add_context(page.src_url, page.path)
        return paginator
        
    def data(self):
        return {}


    async def render_component(self, name, props={}, slots=None):
        #print(self.__dict__)
        if name == self.name:
            component = self.__class__
        elif name in self.registered_components:
            component = self.registered_components[name]
        else:
            component = self.global_components[name]

        new_props = copy(self.props)
        new_props.update(props)
        new_props.update({'v_view': self.v_view })
        vu = await component.produce(new_props)
        return await vu.render(slots)

    def render_slot(self, slots, name='default'):
        if slots:
            return slots[name]

    async def render_view(self, name='default'):
        #TODO: Pass in props
        view = self.v_view.children[name]
        props = copy(self.props)
        props.update({'v_view': view })
        vu = await view.create_vu()
        #print(vu.__dict__)
        return await vu.render()

    @classmethod
    def resolve(self, ref):
        component = ref if callable(ref) else self.create_class(ref)
        return component

    @classmethod
    def create_app(self, ref, super_class=None):
        from .app import App
        if not super_class:
            super_class = App

        app_class = self.create_class(ref, super_class)
        return app_class

    @classmethod
    def create_class(self, ref, super_class=None):
        src_path = to_path(ref)
        if src_path.suffix == '':
            src_path = src_path.with_suffix('.vue')
        src_stat = os.stat(src_path)

        dst_path = Path(f"build/{'/'.join(src_path.parts[1:])}").with_suffix('.py')
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        if not dst_path.is_file():
            dst_path.touch()
        dst_stat = os.stat(dst_path)

        module_name = '.'.join(dst_path.parts[1:])
        #print(module_name)

        if src_path in self.component_cache:
            return self.component_cache[src_path]
        if not super_class:
            super_class = Vue

        force = True
        if force or src_stat.st_mtime > dst_stat.st_mtime:
            compiler = Compiler(src_path, dst_path)
            compiler.compile()
            attrs = compiler.attrs
        else:
            attrs = {}
        #print(code)
        #print(dir(sys.modules[__name__]))
        #print(sys.modules[__name__].__dict__)

        spec = importlib.util.spec_from_file_location(module_name, dst_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module 
        spec.loader.exec_module(module)

        #attrs = {}
        for key in dir(module):
            #print(key)
            if key.startswith('__'):
                continue
            attrs[key] = module.__dict__[key]

        #class type(name, bases, dict, **kwds)
        component = type(module_name, (super_class,), attrs)
        #component = type(src_path.stem, (super_class,), attrs)
        self.component_cache[src_path] = component
        return component
