import re

from .lexer import Lexer
from .inline_lexer import InlineScanner
from .tokens import *

class TableScanner(InlineScanner):
    #r_pipe = re.compile(r'\|')
    r_pipe = re.compile(r'\|( +)?')
    #r_separator = re.compile(r'--?-+')
    r_separator = re.compile(r'--?-+( +)?')

    def scan(self):
        self.scan_row()
        return self.output

    def scan_row(self, terminator = lambda sc: sc.match('\n')):
        while self.cursor < len(self.input):
            if terminator(self):
                return True
            if not (
                self.consume(self.r_pipe, PIPE) or
                self.consume(self.r_separator, TSEPARATOR)
                ):
                self.scan_inline(lambda sc: sc.consume(self.r_pipe, PIPE) or sc.match('\n'))
        return False

class TableLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<PIPE>^\|)', 'PIPE'),
    ]

    def tokenize(self, text, lineno=1, index=0):
        ctx = TableScanner(text, lineno, index)
        return ctx.scan()

    '''
    @_(r'\|')
    def PIPE(self, t):
        return t

    @_(r'--?-+')
    def TSEPARATOR(self, t):
        return t

    @_(r'[\w\d]+')
    def TEXT(self, t):
        return t
    '''