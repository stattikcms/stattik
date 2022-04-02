import sly

from .lexer import Lexer

class TextLexer(Lexer):
    tokens = Lexer.tokens

    def __init__(self):
        super().__init__()

    @_(r'\r?\n+')
    def NEWLINE(self, t):
        return t

    @_(r'\*\*\*.+\*\*\*')
    def BOLDITALIC(self, t):
        t.value = t.value[3:-3]
        return t

    @_(r'\*\*.+\*\*')
    def BOLD(self, t):
        t.value = t.value[2:-2]
        return t

    @_(r'\*.+\*')
    def ITALIC(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r'\[([\w\s\d]+)\]\(((?:\/|https?:\/\/)[\w\d./?=#]+)\)$')
    def LINK(self, t):
        return t

    @_(r'.')
    def SPAN(self, t):
        return t