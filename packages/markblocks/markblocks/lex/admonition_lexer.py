import re

from .lexer import Lexer
from .inline_lexer import InlineScanner
from .tokens import *

class AdmonitionScanner(InlineScanner):
    r_ad = re.compile(r'^!!!( +)?')
    r_name = re.compile(r'[a-zA-Z0-9_]+')
    r_ws = re.compile(r' +')
    r_string = re.compile(r'\".+\"')

    def scan(self):
        self.scan_ad()
        return self.output

    def scan_ad(self):
        if not self.consume_backup(self.r_ad, ADMONITION):
            return False
        if not self.consume(self.r_name, NAME):
            return self.fail()
        self.consume(self.r_ws, WS)

        def t_string(t):
            t.value = t.value[1:-1]
            return t

        self.consume(self.r_string, STRING, t_string)

        return self.succeed()

class AdmonitionLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<ADMONITION>^!!!( +)?)', 'ADMONITION'),
    ]

    def tokenize(self, text, lineno=1, index=0):
        ctx = AdmonitionScanner(text, lineno, index)
        return ctx.scan()

    '''
    @_(r'^!!!( +)?')
    def ADMONITION(self, t):
        return t

    @_(r'[a-zA-Z0-9_]+')
    def NAME(self, t):
        return t

    @_(r'\".+\"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r' +')
    def WS(self, t):
        return t
    '''