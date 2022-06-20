import unittest
import itertools

from markblocks.data import load

from markblocks.lex.multilexer import MultiLexer
from markblocks.lex.inline_lexer import InlineLexer
from markblocks.lex.heading_lexer import HeadingLexer
from markblocks.lex.blockquote_lexer import BlockquoteLexer

from markblocks.parse.parser import Parser
from markblocks.ast.node import AstEncoder

from markblocks.render.default_renderer import DefaultRenderer

class Test(unittest.TestCase):
    def test(self):
        filename = "blockquote.md"
        with load(filename) as fh:
            s = fh.read()

        print("##start##")
        print(s)
        print("##end##")

        lexer = MultiLexer()

        lexer.add_lexer(InlineLexer(), default=True)
        lexer.add_lexer(HeadingLexer())
        lexer.add_lexer(BlockquoteLexer())

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

        renderer = DefaultRenderer()
        result = renderer.render(ast)
        print(result)

if __name__ == "__main__":
    unittest.main()
