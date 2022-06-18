from .lexer import Lexer
from .scanner import Scanner
from .tokens import *

class InlineScanner(Scanner):
    def scan_inline(self, terminator = '\n'):
        while self.cursor < len(self.input):
            if self.match(terminator):
                return True
            if not (
                self.scan_code() or
                self.scan_image() or
                self.scan_link()
                ):
                self('TEXT', self.value)
                self.advance()
        return False

    def scan_code(self):
        if not self.match('`'):
            return False
        self.backup()
        self(BACKTICK, self.value)
        self.advance()

        if not self.scan_inline('`'):
            return self.fail()
        self(BACKTICK, self.value)
        self.advance()
        return True

    def scan_image(self):
        if not self.match('!'):
            return False
        self.backup()
        self(BANG, self.value)
        self.advance()

        if not self.scan_link():
            return self.fail()
        return True
        

    def scan_link(self):
        if not self.match('['):
            return False
        self.backup()
        self(LBRACE, self.value)
        self.advance()

        if not self.scan_inline(']'):
            return self.fail()
        self(RBRACE, self.value)
        self.advance()

        if not self.match('('):
            return self.fail()
        self(LPAREN, self.value)
        self.advance()

        if not self.scan_inline(')'):
            return self.fail()
        self(RPAREN, self.value)
        self.advance()
        return True


class InlineLexer(Lexer):
    tokens = Lexer.tokens

    def tokenize(self, text, lineno=1, index=0):
        ctx = InlineScanner(text)
        ctx.scan_inline()
        return ctx.output
