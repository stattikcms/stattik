import inspect

from .resolver import *

class Schema():
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        if parent:
            parent.add_child(self)
            self.db = parent.db
        else:
            self.db = self

    @classmethod
    def produce(cls, parent=None):
        schema = cls(parent)
        return schema

    def add_child(self, schema):
        self.children.append(schema)

    def register(self):
        for entry in self.entries:
            entry.register(self)
        for child in self.children:
            child.register()

    def add(self, r):
        self.entries.append(r)

    @classmethod
    def __collect_functions(cls, definitions):
        '''
        Collect all of the tagged grammar entries
        '''
        entries = [ (name, value) for name, value in definitions
                  if callable(value) and hasattr(value, 'name') ]
        return entries

    @classmethod
    def _build(cls, definitions):
        if vars(cls).get('_build', False):
            return

        # Collect all of the entry functions from the class definition
        functions = cls.__collect_functions(definitions)

        cls.entries = cls.__build_entries(functions)

    @classmethod
    def __build_entries(cls, functions):
        entries = []
        errors = ''
        for name, func in functions:
            entry = cls._build_entry(func)
            entries.append(entry)
        return entries

    @classmethod
    def _build_entry(cls, func):
        tag = func.tag
        name = func.name
        prodname = func.__name__
        unwrapped = inspect.unwrap(func)
        filename = unwrapped.__code__.co_filename
        lineno = unwrapped.__code__.co_firstlineno

        logger.debug(f"_build_entry:tag:  {tag}")
        logger.debug(f"_build_entry:name:  {name}")
        logger.debug(f"_build_entry:prodname:  {prodname}")
        logger.debug(f"_build_entry:unwrapped:  {unwrapped}")

        entry = entry_factories[tag](cls, name, func, prodname=prodname, filename=filename, lineno=lineno)

        logger.debug(f"_build_entry:entry:  {entry}")
        return entry
