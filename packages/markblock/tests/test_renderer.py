import unittest
from markblock.render.renderer import Renderer
from markblock.compile.ast.node import *
from markblock.visitor import Visitor

data = Ul([
    Text([
        Span('Hello World')
    ])
])


class MyRenderer(Renderer):
    def Ul(self, node):
        print(node)
        self('<ul>')
        with self.scope:
            for child in node.children:
                self('<li>')
                with self.scope:
                    self.visit(child)
                self('</li>')
        self('</ul>')

    Text = Visitor.visits

    Span = Renderer.value_
    

class Test(unittest.TestCase):
    def test(self):
        renderer = MyRenderer()
        result = renderer.render(data)
        print(result)


if __name__ == "__main__":
    unittest.main()
