import sys
from pathlib import Path

import lark
from lark.exceptions import UnexpectedInput, UnexpectedToken

from markblocks.lex.lexer import Lexer
import markblocks.ast.node  as yy


class TokenStream(lark.lexer.Lexer):
    '''Feed tokens from MultiLexer straight through to the Lark parser.'''
    def __init__(self, lexer_conf):
        pass

    def lex(self, tokens):
        for t in tokens:
            value = t.value if t.value is not None else ''
            yield lark.Token(t.type, value, start_pos=t.index, end_pos=t.end, line=t.lineno)


class AstBuilder(lark.Transformer):
    def start(self, p):
        return yy.Document(p[0].children)

    def body(self, p):
        return p[1]

    def block_group_new(self, p):
        return yy.Block([p[0]])

    def block_group_add(self, p):
        p[0].add(p[1])
        return p[0]

    def line(self, p):
        return p[0]

    def empty_line(self, p):
        return yy.Empty()

    def heading_u(self, p):
        level = 1 if p[2].type == 'H1U' else 2
        return yy.Heading(level, p[0].children)

    def heading(self, p):
        level = int(p[0].type[1])
        return yy.Heading(level, p[1].children)

    # Inlines

    def text(self, p):
        return yy.Text(p[0].value)

    def code_span(self, p):
        return yy.CodeSpan(p[1].value)

    def bold_italic(self, p):
        return yy.BoldItalic(p[1].value)

    def bold(self, p):
        return yy.Bold(p[1].value)

    def italic(self, p):
        return yy.Italic(p[1].value)

    def emoji(self, p):
        return yy.Emoji(p[0].value)

    def link(self, p):
        return yy.Link(p[1], p[4].value)

    def image(self, p):
        return yy.Image(p[2].value, p[5].value)

    def inline_group_add(self, p):
        p[0].add(p[1])
        return p[0]

    def inline_group_new(self, p):
        return yy.InlineGroup([p[0]])

    def paragraph(self, p):
        return yy.Paragraph(p[0].children)

    def paragraph_join(self, p):
        return yy.Paragraph(p[0].children + p[1].children)

    # Block quotes

    def blockquote(self, p):
        return yy.Blockquote(p[1].children)

    def blockquote_body(self, p):
        return yy.Blockquote(p[2].children)

    def blockquote_inline_body(self, p):
        return yy.Blockquote(p[1].children + p[3].children)

    # Lists

    def list_item(self, p):
        return p[1]

    def list_item_body(self, p):
        p[1].children = p[1].children + p[3].children
        return p[1]

    def list_add(self, p):
        p[0].add(p[1])
        return p[0]

    def ul(self, p):
        return yy.Ul([p[0]])

    def ol(self, p):
        return yy.Ol([p[0]])

    def tl_item(self, p):
        checked = 'x' in p[0].value
        return yy.TlItem(p[1], checked)

    def tl(self, p):
        return yy.Tl([p[0]])

    # Fence

    def fence(self, p):
        if p[1].type == 'NAME':
            return yy.Fence(p[0].value, p[1].value)
        return yy.Fence(p[0].value)

    # Admonition

    def admonition_title(self, p):
        return yy.Admonition(p[5].children, p[1].value, p[3].value)

    def admonition(self, p):
        return yy.Admonition(p[3].children, p[1].value)

    # Table

    def t_cell(self, p):
        return p[1]

    def t_sep_cell(self, p):
        return p[1].value

    def list_append(self, p):
        p[0].append(p[1])
        return p[0]

    def list_new(self, p):
        return [p[0]]

    def t_row(self, p):
        return yy.TRow(p[0])

    def t_body(self, p):
        return yy.TBody(p[0])

    def t_head(self, p):
        return yy.THead(p[0].children, p[1])

    def table(self, p):
        return yy.Table([p[0], p[1]])


def _grammar():
    declare = '%declare ' + ' '.join(sorted(Lexer.tokens))
    return declare + '\n' + (Path(__file__).parent / 'markblocks.lark').read_text()


class Parser:
    _lark = None

    def __init__(self):
        if not Parser._lark:
            Parser._lark = lark.Lark(
                _grammar(),
                parser='lalr',
                lexer=TokenStream,
                transformer=AstBuilder(),
            )

    def error(self, token):
        if token is not None:
            lineno = getattr(token, 'line', 0)
            if lineno:
                sys.stderr.write(f'lark: Syntax error at line {lineno}, index {token.start_pos}, token={token.type}, value={token.value}\n')
            else:
                sys.stderr.write(f'lark: Syntax error, token={token.type}, value={token.value}\n')
        else:
            sys.stderr.write('lark: Parse error in input. EOF\n')

    def parse(self, tokens):
        try:
            return self._lark.parse(tokens)
        except UnexpectedToken as e:
            self.error(e.token if e.token.type != '$END' else None)
        except UnexpectedInput as e:
            self.error(None)
        return None
