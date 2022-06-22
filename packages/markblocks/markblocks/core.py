import itertools

from .lex.multilexer import MultiLexer
from .lex.inline_lexer import InlineLexer
from .lex.heading_lexer import HeadingLexer
from .lex.taglexer import TagLexer
from .lex.blockquote_lexer import BlockquoteLexer
from .lex.list_lexer import ListLexer
from .lex.fence_lexer import FenceLexer
from .lex.admonition_lexer import AdmonitionLexer
from .lex.table_lexer import TableLexer

from .parse.parser import Parser
from .ast.node import AstEncoder

from .render.default_renderer import DefaultRenderer


class Markblocks:
    def convert(self, text, renderer = DefaultRenderer()):
        if not text:
            return ''
        lexer = MultiLexer()

        lexer.add_lexer(InlineLexer(), default=True)
        lexer.add_lexer(HeadingLexer())
        lexer.add_lexer(TagLexer())
        lexer.add_lexer(BlockquoteLexer())
        lexer.add_lexer(ListLexer())
        lexer.add_lexer(FenceLexer())
        lexer.add_lexer(AdmonitionLexer())
        lexer.add_lexer(TableLexer())

        tokens = lexer.tokenize(text)

        tokens, tokens2 = itertools.tee(tokens)
        #for tok in tokens2:
        #    print(tok)

        parser = Parser()
        
        # ast = parser.parse(s, debug=1)
        ast = parser.parse(tokens)
        #print(AstEncoder(indent=2).encode(ast))
        if not ast:
            return None
        result = renderer.render(ast)
        #print(result)
        return result
