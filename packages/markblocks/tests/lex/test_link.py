import unittest

import sly

from markblocks.data import load
from markblocks.lex.inline_lexer import InlineLexer

class Test(unittest.TestCase):
    def test(self):
        filename = "link.md"

        with load(filename) as fh:
            text = fh.read()
            
        lexer = InlineLexer()

        lines = text.splitlines(True)

        for line in lines:
            tokens = lexer.tokenize(line)
            for tok in tokens:
                print(tok)


if __name__ == "__main__":

    Test().test()
