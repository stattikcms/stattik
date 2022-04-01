import unittest
import itertools

from markblock.data import load

from markblock.compile.lex.multilexer import MultiLexer
from markblock.compile.lex.textlexer import TextLexer
from markblock.compile.lex.headinglexer import HeadingLexer
from markblock.compile.lex.taglexer import TagLexer

from markblock.compile.parse.parser import Parser
from markblock.compile.ast.node import AstEncoder


class Test(unittest.TestCase):
    def test(self):
        filename = "paragraph.md"
        with load(filename) as fh:
            s = fh.read()

        print("##start##")
        print(s)
        print("##end##")

        lexer = MultiLexer()
        lexer.add_lexer(TextLexer(), default=True)
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
