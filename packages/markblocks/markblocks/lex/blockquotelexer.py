from .lexer import Lexer

class BlockquoteLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<BLOCKQUOTE>^>( +)?)', 'BLOCKQUOTE'),
    ]
    def __init__(self):
        super().__init__()

    @_(r'\r?\n+')
    def NEWLINE(self, t):
        return t

    @_(r'^>( +)?')
    def BLOCKQUOTE(self, t):
        return t

    @_(r'.')
    def SPAN(self, t):
        return t