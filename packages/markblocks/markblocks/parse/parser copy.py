import sys
import sly
import re

from markblocks.lex.lexer import Lexer
import markblocks.ast.node  as yy

class Parser(sly.Parser):

    tokens = Lexer.tokens

    def __init__(self):
        super().__init__()

    def error(self, token):
        if token:
            lineno = getattr(token, 'lineno', 0)
            if lineno:
                sys.stderr.write(f'sly: Syntax error at line {lineno}, index {token.index}, token={token.type}, value={token.value}\n')
            else:
                sys.stderr.write(f'sly: Syntax error, token={token.type}, value={token.value}\n')
        else:
            sys.stderr.write('sly: Parse error in input. EOF\n')


    @_('Document')
    def File(self, p):
        return p.Document

    @_('Body')
    def Document(self, p):
        return yy.Document(p.Body.children)

    @_('INDENT DEDENT')
    def Block(self, p):
        return yy.Block()

    @_('INDENT Body DEDENT')
    def Block(self, p):
        return p.Body

    @_('Line')
    def Body(self, p):
        return yy.Block([p.Line])

    @_('Body Line')
    def Body(self, p):
        p.Body.add(p.Line)
        return p.Body

    @_('Statement', 'Expression', 'TERMINATOR')
    def Line(self, p):
        if p[0]:
            return p[0]
        return yy.Empty()

    '''
    @_('TERMINATOR')
    def Expression(self, p):
        return yy.Empty()
    '''

    @_('TextElementList TERMINATOR H1U TERMINATOR')
    def HeadingU(self, p):
        return yy.Heading(1, p[0])

    @_('TextElementList TERMINATOR H2U TERMINATOR')
    def HeadingU(self, p):
        return yy.Heading(2, p[0])

    @_('H1 TextElementList TERMINATOR')
    def Heading(self, p):
        return yy.Heading(1, p[1])

    @_('H2 TextElementList TERMINATOR')
    def Heading(self, p):
        return yy.Heading(2, p[1])

    @_('H3 TextElementList TERMINATOR')
    def Heading(self, p):
        return yy.Heading(3, p[1])

    @_('TAG Expression')
    def Tag(self, p):
        return yy.ImportStmt(p.Expression)

    @_('HeadingU', 'Paragraph', 'Blockquote', 'Ul', 'Ol', 'Fence', 'Admonition', 'Table')
    def Statement(self, p):
        return p[0]

    @_('Tag')
    def Statement(self, p):
        return p[0]

    @_('Heading')
    def Expression(self, p):
        return p[0]

    @_('TEXT')
    def Span(self, p):
        return yy.Span(p[0])

    @_('BOLD')
    def Bold(self, p):
        return yy.Bold(p[0])

    @_('ITALIC')
    def Italic(self, p):
        return yy.Italic(p[0])

    @_('BOLDITALIC')
    def BoldItalic(self, p):
        return yy.BoldItalic(p[0])

    @_('EMOJI')
    def Emoji(self, p):
        return yy.Emoji(p[0])

    @_('LINK')
    def Link(self, p):
        r = re.compile(r'\[(?P<TEXT>([^\]]+))\]\((?P<LINK>(?:\/|https?:\/\/)[\w\d./?=#|?|&|=|-]+)\)')
        m = r.match(p[0])
        return yy.Link(m['TEXT'], m['LINK'])

    @_('IMAGE')
    def Image(self, p):
        r = re.compile(r'\!\[(?P<TEXT>([\w\s\d|#|-]+))\]\((?P<LINK>(?:\/|https?:\/\/)[\w\d./?=#|?|&|=|-]+)\)')
        m = r.match(p[0])
        return yy.Image(m['TEXT'], m['LINK'])

    @_('Span', 'Bold', 'Italic', 'BoldItalic', 'Emoji', 'Link', 'Image')
    def TextElement(self, p):
        return p[0]

    @_('TextElementList TextElement')
    def TextElementList(self, p):
        p[0].append(p[1])
        return p[0]

    @_('TextElement')
    def TextElementList(self, p):
        return [p[0]]

    @_('TextList Text')
    def TextList(self, p):
        p[0].append(p[1])
        return p[0]

    @_('Text')
    def TextList(self, p):
        return [p[0]]

    @_('TextList')
    def Paragraph(self, p):
        return yy.Paragraph(p[0])

    @_('TextElementList TERMINATOR')
    def Text(self, p):
        return yy.Text(p[0])

    # Block quotes

    @_('BLOCKQUOTE Text', 'BLOCKQUOTE Block')
    def BlockquoteItem(self, p):
        return p[1]

    @_('BLOCKQUOTE TERMINATOR')
    def BlockquoteItem(self, p):
        return yy.Empty()

    @_('Block')
    def BlockquoteItem(self, p):
        return p[0]

    @_('BlockquoteList BlockquoteItem')
    def BlockquoteList(self, p):
        p[0].append(p[1])
        return p[0]

    @_('BlockquoteItem')
    def BlockquoteList(self, p):
        return [p[0]]

    @_('BlockquoteList', 'BlockquoteList TERMINATOR')
    def Blockquote(self, p):
        return yy.Blockquote(p[0])

    # Unordered List

    @_('UL Text', 'UL Block')
    def UlItem(self, p):
        return p[1]

    @_('UL TERMINATOR')
    def UlItem(self, p):
        return yy.Empty()

    @_('Block')
    def UlItem(self, p):
        return p[0]

    @_('UlList UlItem')
    def UlList(self, p):
        p[0].append(p[1])
        return p[0]

    @_('UlItem')
    def UlList(self, p):
        return [p[0]]

    @_('UlList', 'UlList TERMINATOR')
    def Ul(self, p):
        return yy.Ul(p[0])

# Ordered List

    @_('OL Text', 'OL Block')
    def OlItem(self, p):
        return p[1]

    @_('OL TERMINATOR')
    def OlItem(self, p):
        return yy.Empty()

    @_('Block')
    def OlItem(self, p):
        return p[0]

    @_('OlList OlItem')
    def OlList(self, p):
        p[0].append(p[1])
        return p[0]

    @_('OlItem')
    def OlList(self, p):
        return [p[0]]

    @_('OlList', 'OlList TERMINATOR')
    def Ol(self, p):
        return yy.Ol(p[0])

    # Fence
    @_('FENCE TERMINATOR')
    def Fence(self, p):
        return yy.Fence(p[0])

    @_('FENCE NAME TERMINATOR')
    def Fence(self, p):
        return yy.Fence(p[0], p[1])

    @_('ADMONITION NAME WS STRING TERMINATOR Block')
    def Admonition(self, p):
        return yy.Admonition(p.Block.children, p.NAME, p.STRING)

    @_('ADMONITION NAME TERMINATOR Block')
    def Admonition(self, p):
        return yy.Admonition(p.Block.children, p.NAME)

# Table

    @_('PIPE Span')
    def TCell(self, p):
        return p[1]

    @_('TRowList TCell')
    def TRowList(self, p):
        p[0].append(p[1])
        return p[0]

    @_('TCell')
    def TRowList(self, p):
        return [p[0]]

    @_('TRowList TERMINATOR')
    def TRow(self, p):
        return yy.TRow(p[0])

    # Separator
    @_('PIPE TSEPARATOR')
    def TSepCell(self, p):
        return p[1]

    @_('TSepRowList TSepCell')
    def TSepRowList(self, p):
        p[0].append(p[1])
        return p[0]

    @_('TSepCell')
    def TSepRowList(self, p):
        return [p[0]]

    @_('TSepRowList TERMINATOR')
    def TSepRow(self, p):
        return yy.TRow(p[0])

    '''
    # Table Header
    @_('TRow TSepRow TERMINATOR')
    def THeader(self, p):
        return yy.TRow(p[0])
    '''
    # Table
    @_('TableList TRow', 'TableList TSepRow')
    def TableList(self, p):
        p[0].append(p[1])
        return p[0]

    @_('TRow', 'TSepRow')
    def TableList(self, p):
        return [p[0]]

    @_('TableList', 'TableList TERMINATOR')
    def TBody(self, p):
        return yy.TBody(p[0])

    @_('TRow TSepRow')
    def THead(self, p):
        return yy.THead(p[0].children, p[1])

    @_('THead TBody')
    def Table(self, p):
        return yy.Table([p[0], p[1]])