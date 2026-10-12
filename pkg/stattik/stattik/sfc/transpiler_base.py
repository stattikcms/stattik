import sys, types

import re
from string import capwords

from stattik.scope import Scope, Fragment, Css

from .elements import elements

class TranspilerBase:
    def __init__(self):
        self.scopes = []
        self.src_path = None

    def __str__(self):
        return str(self.scope)

    @property
    def scope(self):
        return self.scopes[-1]
    
    def begin(self, node):
        self.scopes.append(Scope(node))

    def begin_fragment(self, node):
        self.scopes.append(Fragment(node))

    def end(self):
        return self.scopes.pop()
    '''
    def iscomponent(self, name):
        if self.kebab_to_pascal(name) == self.src_path.stem:
            return True
        return self.module and hasattr(self.module, 'components') and self.kebab_to_pascal(name) in self.module.components
    '''
    def iscomponent(self, name):
        if not isinstance(name, str):
            return False
        return not name in elements

    def snake(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def snake_to_pascal(self, string):
        result = capwords(string.replace('_',' '))
        result = re.replace(' ','')
        return result

    def kebab(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

    def kebab_to_pascal(self, string):
        result = capwords(string.replace('-',' '))
        result = result.replace(' ','')
        return result

    def _expr_code(self, text):
        return f'{{eval("{text}", globals(), dict(self.__dict__, **locals()))}}'

    def compile_module(self, path, code):
        _module = types.ModuleType(str(path))
        exec(code, _module.__dict__)
        return _module