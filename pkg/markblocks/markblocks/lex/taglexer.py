from .lexer import Lexer

class TagLexer(Lexer):
    #tokens = { H3, H2, H1 }
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<TAG>^:)', 'TAG'),
    ]

    def __init__(self):
        super().__init__()

    @_(r':')
    def TAG(self, t):
        return t

    @_(r'=')
    def ASSIGN(self, t):
        return t

    @_(r'.')
    def TEXT(self, t):
        return t
