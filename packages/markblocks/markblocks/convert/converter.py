import itertools

from markblocks.lex.multilexer import MultiLexer
from markblocks.lex.textlexer import TextLexer
from markblocks.lex.headinglexer import HeadingLexer
from markblocks.lex.taglexer import TagLexer
from markblocks.lex.blockquotelexer import BlockquoteLexer
from markblocks.lex.listlexer import ListLexer
from markblocks.lex.fencelexer import FenceLexer
from markblocks.lex.admonition_lexer import AdmonitionLexer

from markblocks.parse.parser import Parser
from markblocks.ast.node import AstEncoder

from markblocks.render.default_renderer import DefaultRenderer


class Converter:
    def convert(self, text, renderer = DefaultRenderer()):
        lexer = MultiLexer()

        lexer.add_lexer(TextLexer(), default=True)
        lexer.add_lexer(HeadingLexer())
        lexer.add_lexer(TagLexer())
        lexer.add_lexer(BlockquoteLexer())
        lexer.add_lexer(ListLexer())
        lexer.add_lexer(FenceLexer())
        lexer.add_lexer(AdmonitionLexer())

        tokens = lexer.tokenize(text)

        tokens, tokens2 = itertools.tee(tokens)
        #for tok in tokens2:
        #    print(tok)

        parser = Parser()
        
        # ast = parser.parse(s, debug=1)
        ast = parser.parse(tokens)
        #print(AstEncoder(indent=2).encode(ast))

        result = renderer.render(ast)
        #print(result)
        return result
