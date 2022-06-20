import re

import sly

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

    def consume(self, value, token, backup=False):
        match = self.match(value)
        if not match:
            return False
        if backup:
            self.backup()
        if isinstance(match, re.Match):
            end = match.span()[1]
            self(token, self.input[self.cursor:self.cursor+end])
            self.advance(end)
            return True
        self(token, self.value)
        self.advance(len(value))
        return True

    '''
    def match(self, value):
        return self.value == value        
    '''
    def match(self, value):
        if isinstance(value, re.Pattern):
            match = value.match(self.input[self.cursor:-1])
            return match
        return self.input[self.cursor:self.cursor + len(value)] == value    

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
