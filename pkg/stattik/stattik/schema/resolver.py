from loguru import logger

class Entry:
    def __init__(self, schema_class, name, action, prodname=None, filename=None, lineno=None):
        self.schema_class = schema_class
        self.name = name
        self.action = action
        self.prodname = prodname
        self.filename = filename
        self.lineno = lineno

    def register(self, schema):
        pass

class Resolver(Entry):
    pass

class Source(Entry):
    pass

class QueryResolver(Resolver):
    def register(self, schema):
        schema.db.query_type.set_field(self.name, lambda *args, **kwargs: self.action(schema, *args, **kwargs))

class MutationResolver(Resolver):
    def register(self, schema):
        schema.db.mutation_type.set_field(self.name, lambda *args, **kwargs: self.action(schema, *args, **kwargs))

class SubscriptionResolver(Resolver):
    def register(self, schema):
        schema.db.subscription_type.set_field(self.name, lambda *args, **kwargs: self.action(schema, *args, **kwargs))

class SubscriptionSource(Source):
    def register(self, schema):
        schema.db.subscription_type.set_source(self.name, lambda *args, **kwargs: self.action(schema, *args, **kwargs))

entry_factories = {
    "query": QueryResolver,
    "mutation": MutationResolver,
    "subscription": SubscriptionResolver,
    "source": SubscriptionSource,
}
