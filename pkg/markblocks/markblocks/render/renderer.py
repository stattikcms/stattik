from .renderer_base import RendererBase

class Style:
    pass

class Indented(Style):
    def __init__(self, renderer) -> None:
        super().__init__()
        self.renderer = renderer

    def __enter__(self):
        self.renderer.scope.indent()

    def __exit__(self, type, value, traceback):
        self.renderer.scope.dedent()

class Inlined(Style):
    def __init__(self, renderer) -> None:
        super().__init__()
        self.renderer = renderer

    def __enter__(self):
        self.renderer.scope.inlined = True

    def __exit__(self, type, value, traceback):
        self.renderer.scope.inlined = False
        self.renderer.scope.nl()


class Renderer(RendererBase):
    def __init__(self):
        super().__init__()
        self.indented = Indented(self)
        self.inlined = Inlined(self)

    def render(self, root):
        self.begin(root)
        self.visit(root)
        result = str(self)
        self.end()
        return result

    def value_(self, node):
        self(node.value)

    def Empty(self, node):
        return