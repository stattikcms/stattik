class MetaNode(type):
    nodeCount = 0
    def __init__(cls, name, bases, attr):
        cls.nodeCount = 0

    @classmethod
    def node(cls, name):
        index = cls.nodeCount
        cls.nodeCount += 1

        def getter(self):
            return self.nodes[index]

        def setter(self, val):
            self.nodes[index] = val

        prop = property(getter, setter)
        setattr(cls, name, prop)
