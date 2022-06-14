from .lexer import Lexer

'''
NOT USED (Yet?)
The idea was to possibly have sublexers decompose tokens but this seems like overkill.  Just use Regex
'''

class LinkLexer(Lexer):
    tokens = Lexer.tokens
    def __init__(self):
        super().__init__()

    @_(r'\[')
    def LBRACE(self, t):
        return t

    @_(r'\]')
    def RBRACE(self, t):
        return t

    @_(r'\(')
    def LPAREN(self, t):
        return t

    @_(r'\)')
    def RPAREN(self, t):
        return t
