from loguru import logger

from sqlalchemy.ext.asyncio import async_scoped_session

class Schema:
    Session: async_scoped_session | None = None
    def __init__(self, parent: "Schema | None" = None):
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
