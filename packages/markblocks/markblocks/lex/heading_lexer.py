import re

from .lexer import Lexer
from .inline_lexer import InlineScanner
from .tokens import *

class HeadingScanner(InlineScanner):
    r_h1 = re.compile(r'#( +)?')
    r_h2 = re.compile(r'##( +)?')
    r_h3 = re.compile(r'###( +)?')
    r_h4 = re.compile(r'####( +)?')

    r_h1_u = re.compile(r'==?=+( +)?')
    r_h2_u = re.compile(r'--?-+( +)?')

    def scan(self):
        self.scan_h4() or self.scan_h3() or self.scan_h2() or self.scan_h1() or self.scan_h1_u() or self.scan_h2_u()
        return self.output

    def scan_h1(self):
        if not self.consume_backup(self.r_h1, H1_OPEN):
            return False
        self.scan_inline()
        self(H1_CLOSE, '#')
        return self.succeed()

    def scan_h2(self):
        if not self.consume_backup(self.r_h2, H2_OPEN):
            return False
        self.scan_inline()
        self(H2_CLOSE, '#')
        return self.succeed()

    def scan_h3(self):
        if not self.consume_backup(self.r_h3, H3_OPEN):
            return False
        self.scan_inline()
        self(H3_CLOSE, '#')
        return self.succeed()

    def scan_h4(self):
        if not self.consume_backup(self.r_h4, H4_OPEN):
            return False
        self.scan_inline()
        self(H4_CLOSE, '#')
        return self.succeed()

    def scan_h1_u(self):
        if not self.consume(self.r_h1_u, H1U):
            return False
        return True

    def scan_h2_u(self):
        if not self.consume(self.r_h2_u, H2U):
            return False
        return True

class HeadingLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<H4>^###( +)?)', 'H4'),
        (r'(?P<H3>^###( +)?)', 'H3'),
        (r'(?P<H2>^##( +)?)', 'H2'),
        (r'(?P<H1>^#( +)?)', 'H1'),
        (r'(?P<H1U>^==( +)?)', 'H1U'),
        (r'(?P<H2U>^--( +)?)', 'H2U'),
    ]

    def tokenize(self, text, lineno=1, index=0):
        ctx = HeadingScanner(text, lineno, index)
        return ctx.scan()
    '''
    @_(r'\r?\n+')
    def NEWLINE(self, t):
        return t

    @_(r'###( +)?')
    def H3(self, t):
        return t

    @_(r'##( +)?')
    def H2(self, t):
        return t

    @_(r'--?-+( +)?')
    def H2U(self, t):
        return t

    @_(r'#( +)?')
    def H1(self, t):
        return t

    @_(r'==?=+( +)?')
    def H1U(self, t):
        return t

    @_(r':\w+:')
    def EMOJI(self, t):
        t.value = t.value[1:-1]
        return t

    #@_(r'.+')
    @_(r'.')
    def TEXT(self, t):
        return t
    '''