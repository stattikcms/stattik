class Builder:

    def __init__(self, parent=None):
        self.parent = parent

        if parent:
            self.architect = parent.architect
            self.builders = parent.builders
        else:
            self.architect = self

    def __getitem__(self, key):
        return self.builders[key]

    @property
    def is_deferred(self):
        return False

    @classmethod
    def produce(self, parent, job):
        builder = self(parent, job)
        return builder

    def defer(self, builder, job):
        self.architect.defer(builder, job)

    async def build(self, job):
        pass
