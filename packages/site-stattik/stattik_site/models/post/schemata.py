from stattik.schemata import Connection, Edge, Node


class PostNode(Node):
    def __init__(self, obj):
        super().__init__(obj)

class PostEdge(Edge):
    def __init__(self, obj, node_class=PostNode):
        super().__init__(obj, node_class)

class PostConnection(Connection):
    def __init__(self, objs):
        super().__init__(objs, edge_class=PostEdge, node_class=PostNode)
