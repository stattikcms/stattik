import re

from .lexer import Lexer
from .inline_lexer import InlineScanner
from .tokens import *

class FenceScanner(InlineScanner):
    r_fence = re.compile(r'^```( +)?')
    r_name = re.compile(r'[a-zA-Z0-9_]+')

    def scan(self):
        self.scan_fence()
        return self.output

    def scan_fence(self):
        if not self.consume(self.r_fence, FENCE):
            return False
        self.consume(self.r_name, NAME)
        return True

class FenceLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<FENCE>^```( +)?)', 'FENCE'),
    ]

    def tokenize(self, text, lineno=1, index=0):
        ctx = FenceScanner(text, lineno, index)
        return ctx.scan()
