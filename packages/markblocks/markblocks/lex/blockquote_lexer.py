import re

from .lexer import Lexer
from .inline_lexer import InlineScanner
from .tokens import *

class BlockquoteScanner(InlineScanner):
    r_bq = re.compile(r'^>( +)?')

    def scan(self):
        self.scan_bq()
        return self.output

    def scan_bq(self):
        if not self.consume(self.r_bq, BLOCKQUOTE, backup=True):
            return False
        self.scan_inline()
        #self(H1_CLOSE, '#')
        return self.succeed()

class BlockquoteLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<BLOCKQUOTE>^>( +)?)', 'BLOCKQUOTE'),
    ]

    def tokenize(self, text, lineno=1, index=0):
        ctx = BlockquoteScanner(text, lineno, index)
        return ctx.scan()
    '''
    @_(r'^>( +)?')
    def BLOCKQUOTE(self, t):
        return t

    @_(r'.')
    def TEXT(self, t):
        return t
    '''