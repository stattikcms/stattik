INDENT_STEP = 4

class Scope:
    def __init__(self, node):
        self.node = node
        self.indent_level = 0
        self.indent_step = INDENT_STEP
        self.lines = []

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level -= 1

    def __call__(self, line):
        line = f"{' ' * self.indent_level * self.indent_step}{line}\n"
        self.lines.append(line)

    def nl(self):
        self.lines.append('\n')

    def add(self, scope):
        return self.lines + scope.lines

    def iadd(self, scope):
        self.lines += scope.lines

    def __str__(self):
        return "".join(self.lines)

class Fragment(Scope):
    counter = 0
    def __init__(self, node):
        super().__init__(node)
        self.counter = Fragment.counter
        Fragment.counter += 1

class Css(Scope):
    def __init__(self, node):
        super().__init__(node)
