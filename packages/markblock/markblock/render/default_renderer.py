from .renderer import Renderer
from markblock.compile.ast.node import *
from markblock.visitor import Visitor


class DefaultRenderer(Renderer):

    Document = Visitor.visits

    Block = Visitor.visits

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