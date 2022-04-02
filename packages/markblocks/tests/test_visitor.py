import unittest
from markblocks.visitor import Visitor
from markblocks.ast.node import *

data = Ul([
    Text([
        Span('Hello World')
    ])
])

reducer = lambda x: ''.join(x)

class MyVisitor(Visitor):
    def Ul(self, node, value):
        print(node)
        return f"<ul>{value}</ul>"

    def Text(self, node, value):
        print(node)
        return value

    def Span(self, node, value):
        print(node)
        return node.value
    

class Test(unittest.TestCase):
    def test(self):
        visitor = MyVisitor()
        result = visitor.visit(data, reducer)
        print(result)


if __name__ == "__main__":
    unittest.main()
