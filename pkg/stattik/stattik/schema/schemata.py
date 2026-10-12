class Schemata:
    def __init__(self, typename):
        self.typename = typename
    def wire(self):
        return {}

class Node(Schemata):
    def __init__(self, typename, obj):
        super().__init__(typename)
        self.objekt = obj

    def wire(self):
        result = self.objekt.to_dict()
        result['__typename'] = self.typename,
        return result

class Edge(Schemata):
    def __init__(self, typename, obj):
        super().__init__(f'{typename}Edge')
        self.cursor = ""
        self.node = Node(typename, obj)

    def wire(self):
        result = {
            '__typename': self.typename,
            'cursor': self.cursor,
            'node': self.node.wire()
        }
        return result

class Connection(Schemata): 
    def __init__(self, typename, objs):
        super().__init__(f'{typename}Connection')
        self.edges = []
        self.pageInfo = None
        for obj in objs:
            self.edges.append(Edge(typename, obj))

    def wire(self):
        result = {
            '__typename': self.typename,
            'edges': [edge.wire() for edge in self.edges],
            'pageInfo': self.pageInfo
            }
        return result
