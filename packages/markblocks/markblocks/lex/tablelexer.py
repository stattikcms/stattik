from .lexer import Lexer

class TableLexer(Lexer):
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<PIPE>^\|)', 'PIPE'),
    ]
    def __init__(self):
        super().__init__()


    @_(r'\|')
    def PIPE(self, t):
        return t

    @_(r'--?-+')
    def TSEPARATOR(self, t):
        return t

    #@_(r'.+')
    #@_(r'.')
    #@_(r'[\w\s\d]+')
    @_(r'[\w\d]+')
    def SPAN(self, t):
        return t
