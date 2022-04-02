from .renderer_base import RendererBase

class Renderer(RendererBase):
    def render(self, root):
        self.begin(root)
        self.visit(root)
        result = str(self)
        self.end()
        return result

    def value_(self, node):
        self(node.value)
