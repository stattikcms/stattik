from .lexer import Lexer

class HtmlLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<BLOCKQUOTE>^>( +)?)', 'BLOCKQUOTE'),
    ]
    def __init__(self):
        super().__init__()

    @_(r'^>( +)?')
    def BLOCKQUOTE(self, t):
        return t

    @_(r'.')
    def TEXT(self, t):
        return t