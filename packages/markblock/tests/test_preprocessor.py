import unittest

from markblock.data import load
from markblock.compile.lex.textlexer import TextLexer


class Test(unittest.TestCase):
    def test(self):
        filename = "hello.mb"

        with load(filename) as fh:
            s = fh.read()
            
        lexer = TextLexer()
        tokens = lexer.tokenize(s)
        for tok in tokens:
            print(tok)

if __name__ == "__main__":

    Test().test()
