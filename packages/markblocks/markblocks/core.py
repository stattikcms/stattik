import itertools

from .lex.multilexer import MultiLexer
from .lex.textlexer import TextLexer
from .lex.headinglexer import HeadingLexer
from .lex.taglexer import TagLexer
from .lex.blockquotelexer import BlockquoteLexer
from .lex.listlexer import ListLexer
from .lex.fencelexer import FenceLexer
from .lex.admonition_lexer import AdmonitionLexer

from .parse.parser import Parser
from .ast.node import AstEncoder

from .render.default_renderer import DefaultRenderer


class Markblocks:
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
