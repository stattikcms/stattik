from .lexer import Lexer

class ListLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<UL>^\*( +)?)', 'UL'),
        (r'(?P<OL>^\d+.( +)?)', 'OL'),
    ]
    def __init__(self):
        super().__init__()

    @_(r'^\*( +)?')
    def UL(self, t):
        return t

    @_(r'^\d+.( +)?')
    def OL(self, t):
        return t

    @_(r'.')
    def SPAN(self, t):
        return t