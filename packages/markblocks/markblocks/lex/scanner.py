import sly

class ScannerState:
    def __init__(self, cursor, output=[]):
        self.cursor = cursor
        self.output = output

class Scanner:
    def __init__(self, input) -> None:
        self.input = input
        self.output = []
        self.cursor = 0
        self.states = []

    def backup(self):
        self.states.append(ScannerState(self.cursor, self.output[:]))

    def restore(self):
        state = self.states.pop()
        self.cursor = state.cursor
        self.output = state.output

    def fail(self):
        self.restore()
        return False

    def advance(self):
        self.cursor += 1

    @property
    def value(self):
        return self.input[self.cursor]

    def match(self, value):
        return self.value == value        

    def create_token(self, type, value, lineno=1, index=0):
        tok = sly.lex.Token()
        tok.type = type
        tok.value = value
        tok.lineno = lineno
        tok.index = index
        return tok

    def __call__(self, type, value, lineno=1, index=0):
        tok = self.create_token(type, value, lineno, index)
        self.output.append(tok)
