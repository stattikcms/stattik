class Visitor:
    def visit(self, node):
        fn = getattr(self, node.kind)
        return fn(node)

    def visits(self, node):
        for child in node.children:
            self.visit(child)

    def walk_visit(self, node, reducer):
        return node.walk(lambda node, value: self.visit_node(node, value), reducer)

    def walk_visit_node(self, node, value):
        fn = getattr(self, node.kind)
        return fn(node, value)