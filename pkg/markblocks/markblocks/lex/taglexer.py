import re

from .lexer import Lexer
from .scanner import Scanner
from .tokens import *

class TagScanner(Scanner):
    def scan(self):
        while self.cursor < len(self.input):
            if not (
                self.consume(':', TAG) or
                self.consume('=', 'ASSIGN')
                ):
                self(TEXT, self.value)
                self.advance()
        return self.output

class TagLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<TAG>^:)', 'TAG'),
    ]

    def tokenize(self, text, lineno=1, index=0):
        ctx = TagScanner(text, lineno, index)
        return ctx.scan()
