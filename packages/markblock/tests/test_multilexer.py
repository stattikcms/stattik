import unittest

from markblock.data import load

from markblock.compile.lex.multilexer import MultiLexer
from markblock.compile.lex.textlexer import TextLexer
from markblock.compile.lex.headinglexer import HeadingLexer
from markblock.compile.lex.taglexer import TagLexer

class Test(unittest.TestCase):
    def test(self):
        filename = "tags.mb"

        with load(filename) as fh:
            s = fh.read()
            
        lexer = MultiLexer()
        lexer.add_lexer(TextLexer(), default=True)
        lexer.add_lexer(HeadingLexer())
        lexer.add_lexer(TagLexer())
        tokens = lexer.tokenize(s)
        for tok in tokens:
            print(tok)

if __name__ == "__main__":

    Test().test()

