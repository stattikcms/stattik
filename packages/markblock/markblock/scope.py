INDENT_STEP = 2

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

    def __enter__(self):
        self.indent()

    def __exit__(self, type, value, traceback):
        self.dedent()

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
