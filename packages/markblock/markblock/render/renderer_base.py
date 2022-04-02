from markblock.visitor import Visitor
from markblock.scope import Scope


class RendererBase(Visitor):
    def __init__(self):
        self.scopes = []

    def __str__(self):
        return str(self.scope)

    @property
    def scope(self):
        return self.scopes[-1]

    def indent(self):
        self.scope.indent()

    def dedent(self):
        self.scope.dedent()

    def __enter__(self):
        self.begin()

    def __exit__(self, type, value, traceback):
        self.end()

    def __call__(self, line):
        self.scope(line)

    def begin(self, node):
        self.scopes.append(Scope(node))

    def end(self):
        return self.scopes.pop()
