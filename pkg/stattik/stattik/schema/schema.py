import inspect

from ariadne import make_executable_schema, QueryType, MutationType, SubscriptionType

from .resolver import *

#
# Schema
#

class GrammarError(Exception):
    pass

keywords = ['query', 'mutation', 'subscription', 'source']

class SchemaMetaDict(dict):
    '''
    Dictionary that allows decorated schema entry functions to be overloaded
    '''
    def __setitem__(self, key, value):
        if key in self and callable(value) and hasattr(value, 'name'):
            value.next_func = self[key]
            if not hasattr(value.next_func, 'name'):
                raise GrammarError(f'Redefinition of {key}. Perhaps an earlier {key} is missing @_')
        super().__setitem__(key, value)
    
    def __getitem__(self, key):
        #if key not in self and key.isupper() and key[:1] != '_':
        if key not in self and key.isupper() and not key[:1] in keywords:
            return key.upper()
        else:
            return super().__getitem__(key)

def _query_decorator(name):
     def decorate(func):
         func.tag = 'query'
         func.name = name
         return func
     return decorate

def _mutation_decorator(name):
     def decorate(func):
         func.tag = 'mutation'
         func.name = name
         return func
     return decorate

def _subscription_decorator(name):
     def decorate(func):
         func.tag = 'subscription'
         func.name = name
         return func
     return decorate

def _source_decorator(name):
     def decorate(func):
         func.tag = 'source'
         func.name = name
         return func
     return decorate

class SchemaMeta(type):
    @classmethod
    def __prepare__(meta, *args, **kwargs):
        d = SchemaMetaDict()
        d['query'] = _query_decorator
        d['mutation'] = _mutation_decorator
        d['subscription'] = _subscription_decorator
        d['source'] = _source_decorator

        return d

    def __new__(meta, selfname, bases, attributes):
        #del attributes['_']
        for key in keywords:
            del attributes[key]
        self = super().__new__(meta, selfname, bases, attributes)
        self._build(list(attributes.items()))
        return self

class Schema(metaclass=SchemaMeta):
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        if parent:
            parent.add_child(self)
            self.db = parent.db
        else:
            self.db = self
        self.entries = self.__class__.entries

    @classmethod
    def produce(cls, parent=None):
        schema = cls(parent)
        return schema

    def add_child(self, schema):
        self.children.append(schema)

    def get_gql(self):
        gql = [inspect.getdoc(self)]
        for child in self.children:
            gql.append(child.get_gql())
        return "\n".join(gql)

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

# This is for testing or in case you don't want a database as the root schema

class RootSchema(Schema):
    """
    type Query {
        dummy: Int!
    }
    type Mutation {
        setDummy(val: Int!): Int
    }
    type Subscription {
        dummy: Int
    }
    """
    instance = None

    def __init__(self, parent=None):
        super().__init__(parent)
        Schema.instance = self
        self.query_type = QueryType()
        self.mutation_type = MutationType()
        self.subscription_type = SubscriptionType()

    @classmethod
    def produce(cls):
        if cls.instance:
            return cls.instance
        cls.instance = schema = cls()
        return schema

    def make_executable(self):
        self.register()
        return make_executable_schema(
            self.get_gql(),
            self.query_type,
            self.mutation_type,
            self.subscription_type
        )