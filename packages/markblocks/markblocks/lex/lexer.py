import sly

from . import tokens

class Lexer(sly.Lexer):

    def __init__(self):
        super().__init__()

    def error(self, t):
        print(f"{self.__class__.__name__}: Line {self.lineno}: Bad character '{t.value[0]}'")
        self.index += 1

    def create_token(self, type, value, lineno, index):
        tok = sly.lex.Token()
        tok.type = type
        tok.value = value
        tok.lineno = lineno
        tok.index = index
        return tok


    tokens = tokens.tokens

    # Whitespace
    #@_(r' [ \t]+ ')
    @_(r'^ +')
    def WS(self, t):
        return t
