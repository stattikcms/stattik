from .lexer import Lexer
from .scanner import Scanner
from .tokens import *

class InlineScanner(Scanner):
    def scan(self):
        self.scan_inline()
        return self.output

    def scan_inline(self, terminator = lambda sc: sc.match('\n')):
        while self.cursor < len(self.input):
            if terminator(self):
                return True
            if not (
                self.scan_code() or
                self.scan_emphasis() or
                self.scan_image() or
                self.scan_link()
                ):
                self('TEXT', self.value)
                self.advance()
        return False

    def scan_code(self):
        if not self.consume('`', CODE_SPAN_OPEN, backup=True):
            return False

        if not self.scan_inline(lambda sc: sc.consume('`', CODE_SPAN_CLOSE)):
            return self.fail()

        return self.succeed()

    def scan_emphasis(self):
        if not self.match('*'):
            return False
        return (
            self.scan_bold_italic() or
            self.scan_bold() or
            self.scan_italic()
            )

    def scan_bold_italic(self):
        if not self.consume('***', BOLD_ITALIC_OPEN, backup=True):
            return False

        if not self.scan_inline(lambda sc: sc.consume('***', BOLD_ITALIC_CLOSE)):
            return self.fail()

        return self.succeed()

    def scan_bold(self):
        if not self.consume('**', BOLD_OPEN, backup=True):
            return False

        if not self.scan_inline(lambda sc: sc.consume('**', BOLD_CLOSE)):
            return self.fail()

        return self.succeed()

    def scan_italic(self):
        if not self.consume('*', ITALIC_OPEN, backup=True):
            return False

        if not self.scan_inline(lambda sc: sc.consume('*', ITALIC_CLOSE)):
            return self.fail()

        return self.succeed()

    def scan_image(self):
        if not self.consume('!', BANG, backup=True):
            return False

        if not self.scan_link():
            return self.fail()

        return self.succeed()
        

    def scan_link(self):
        if not self.consume('[', LBRACE, backup=True):
            return False

        if not self.scan_inline(lambda sc: sc.consume(']', RBRACE)):
            return self.fail()

        if not self.consume('(', LPAREN):
            return self.fail()

        if not self.scan_inline(lambda sc: sc.consume(')', RPAREN)):
            return self.fail()

        return self.succeed()


class InlineLexer(Lexer):
    tokens = Lexer.tokens

    def tokenize(self, text, lineno=1, index=0):
        ctx = InlineScanner(text, lineno, index)
        return ctx.scan()
