import unittest

from markblocks.data import load
from markblocks.lex.textlexer import TextLexer


class Test(unittest.TestCase):
    def test(self):
        filename = "hello.md"

        with load(filename) as fh:
            s = fh.read()
            
        lexer = TextLexer()
        tokens = lexer.tokenize(s)
        for tok in tokens:
            print(tok)

if __name__ == "__main__":

    Test().test()
