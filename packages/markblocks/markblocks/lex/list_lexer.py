import re

from .lexer import Lexer
from .inline_lexer import InlineScanner
from .tokens import *

class ListScanner(InlineScanner):
    r_ul = re.compile(r'^\*( +)?')
    r_ol = re.compile(r'^\d+.( +)?')
    r_tl = re.compile(r'^\- \[( |x)\]( +)?')

    def scan(self):
        self.scan_ul() or self.scan_ol() or self.scan_tl()
        return self.output

    def scan_ul(self):
        if not self.consume(self.r_ul, UL):
            return False
        self.scan_inline()

    def scan_ol(self):
        if not self.consume(self.r_ol, OL):
            return False
        self.scan_inline()

    def scan_tl(self):
        if not self.consume(self.r_tl, TL):
            return False
        self.scan_inline()

class ListLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<UL>^\*( +)?)', 'UL'),
        (r'(?P<OL>^\d+.( +)?)', 'OL'),
        (r'(?P<TL>^\- \[( |x)\]( +)?)', 'TL'),
    ]
    def tokenize(self, text, lineno=1, index=0):
        ctx = ListScanner(text, lineno, index)
        return ctx.scan()
    '''
    @_(r'^\*( +)?')
    def UL(self, t):
        return t

    @_(r'^\d+.( +)?')
    def OL(self, t):
        return t

    @_(r'.')
    def TEXT(self, t):
        return t
    '''