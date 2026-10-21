from loguru import logger

class Schema:
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
