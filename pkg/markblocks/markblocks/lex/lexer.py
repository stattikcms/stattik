from . import tokens
from .token import Token

class Lexer:
    tokens = tokens.tokens
    fingerprints = []

    def create_token(self, type, value, lineno, index):
        return Token(type, value, lineno, index, index + len(value))

    def tokenize(self, text, lineno=1, index=0):
        raise NotImplementedError
