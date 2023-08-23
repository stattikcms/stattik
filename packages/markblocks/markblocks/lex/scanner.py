import re

import markblocks.sly as sly

class ScannerState:
    def __init__(self, cursor, output=[]):
        self.cursor = cursor
        self.output = output

class Scanner:
    def __init__(self, input, lineno=1, index=0) -> None:
        self.input = input
        self.lineno = lineno
        self.cursor = index
        self.output = []
        self.states = []

    def backup(self):
        self.states.append(ScannerState(self.cursor, self.output[:]))

    def restore(self):
        state = self.states.pop()
        self.cursor = state.cursor
        self.output = state.output

    def succeed(self):
        self.states.pop()
        return True

    def fail(self):
        self.restore()
        return False

    def advance(self, increment=1):
        self.cursor += increment

    @property
    def value(self):
        return self.input[self.cursor]

    def consume(self, pattern, type, succeed = lambda t: t):
        return self._consume(pattern, type, succeed)

    def consume_backup(self, pattern, type, succeed = lambda t: t):
        return self._consume(pattern, type, succeed, backup=True)

    def _consume(self, pattern, type, succeed = lambda t: t, backup=False):
        match = self.match(pattern)
        if not match:
            return False
        if backup:
            self.backup()
        if isinstance(match, re.Match):
            end = match.span()[1]
            value = self.input[self.cursor:self.cursor+end]
            length = end
        else:
            value = pattern
            length = len(value)

        token = self.create_token(type, value)
        token = succeed(token)
        self.write(token)
        self.advance(length)

        return True

    def match(self, value):
        if isinstance(value, re.Pattern):
            match = value.match(self.input[self.cursor:])
            return match
        return self.input[self.cursor:self.cursor + len(value)] == value    

    def create_token(self, type, value):
        tok = sly.lex.Token()
        tok.type = type
        tok.value = value
        tok.lineno = self.lineno
        tok.index = self.cursor
        tok.end = self.cursor + len(value)
        return tok

    def write(self, token):
        self.output.append(token)

    def __call__(self, type, value):
        token = self.create_token(type, value)
        self.write(token)
