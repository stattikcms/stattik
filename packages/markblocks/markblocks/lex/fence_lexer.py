from .lexer import Lexer

class FenceLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<FENCE>^```( +)?)', 'FENCE'),
    ]
    def __init__(self):
        super().__init__()

    @_(r'^```( +)?')
    def FENCE(self, t):
        return t

    @_(r'[a-zA-Z0-9_]+')
    def NAME(self, t):
        return t
