import unittest

from markblocks.data import load
from markblocks.lex.inline_lexer import InlineLexer

class Test(unittest.TestCase):
    def test(self):
        filename = "hello.md"

        with load(filename) as fh:
            s = fh.read()
            
        lexer = InlineLexer()
        tokens = lexer.tokenize(s)
        for tok in tokens:
            print(tok)

if __name__ == "__main__":
    Test().test()
