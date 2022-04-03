from .lexer import Lexer

class AdmonitionLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<ADMONITION>^!!!( +)?)', 'ADMONITION'),
    ]
    def __init__(self):
        super().__init__()

    @_(r'^!!!( +)?')
    def ADMONITION(self, t):
        return t

    @_(r'[a-zA-Z0-9_]+')
    def NAME(self, t):
        return t

    @_(r'\".+\"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r' +')
    def WS(self, t):
        return t