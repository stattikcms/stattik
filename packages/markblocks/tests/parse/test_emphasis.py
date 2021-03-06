import unittest
import itertools

from markblocks.data import load

from markblocks.lex.multilexer import MultiLexer
from markblocks.lex.inline_lexer import InlineLexer
from markblocks.lex.heading_lexer import HeadingLexer
from markblocks.lex.taglexer import TagLexer

from markblocks.parse.parser import Parser
from markblocks.ast.node import AstEncoder


class Test(unittest.TestCase):
    def test(self):
        filename = "emphasis.md"
        with load(filename) as fh:
            s = fh.read()

        print("##start##")
        print(s)
        print("##end##")

        lexer = MultiLexer()
        lexer.add_lexer(InlineLexer(), default=True)
        lexer.add_lexer(HeadingLexer())
        lexer.add_lexer(TagLexer())

        tokens = lexer.tokenize(s)
        tokens, tokens2 = itertools.tee(tokens)
        for tok in tokens2:
            print(tok)

        parser = Parser()
        
        # ast = parser.parse(s, debug=1)
        ast = parser.parse(tokens)
        # print ast
        # pprint.pprint(ast)
        # json.dumps(ast)
        print(AstEncoder(indent=2).encode(ast))


if __name__ == "__main__":
    unittest.main()
