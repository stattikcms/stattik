import sys
import sly
import re

from markblocks.lex.lexer import Lexer
import markblocks.ast.node  as yy

class Parser(sly.Parser):
    debugfile = 'parser_debug.txt'
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
        return p[0]

    @_('BlockGroup')
    def Document(self, p):
        return yy.Document(p[0].children)

    '''
    @_('INDENT DEDENT')
    def Block(self, p):
        return yy.Block()
    '''

    @_('INDENT BlockGroup DEDENT')
    def Body(self, p):
        return p[1]

    @_('LeafBlock', 'ContainerBlock')
    def Block(self, p):
        return p[0]

    @_('Block')
    def BlockGroup(self, p):
        return yy.Block([p[0]])

    @_('BlockGroup Line')
    def BlockGroup(self, p):
        p.BlockGroup.add(p[1])
        return p.BlockGroup
    
    @_('Block', 'TERMINATOR')
    def Line(self, p):
        if p[0]:
            return p[0]
        return yy.Empty()

    @_('InlineGroup TERMINATOR H1U TERMINATOR')
    def HeadingU(self, p):
        return yy.Heading(1, p[0])

    @_('InlineGroup TERMINATOR H2U TERMINATOR')
    def HeadingU(self, p):
        return yy.Heading(2, p[0])

    @_('H1_OPEN InlineGroup H1_CLOSE TERMINATOR')
    def Heading(self, p):
        return yy.Heading(1, p[1])

    @_('H2_OPEN InlineGroup H2_CLOSE TERMINATOR')
    def Heading(self, p):
        return yy.Heading(2, p[1])

    @_('H3_OPEN InlineGroup H3_CLOSE TERMINATOR')
    def Heading(self, p):
        return yy.Heading(3, p[1])

    @_('H4_OPEN InlineGroup H4_CLOSE TERMINATOR')
    def Heading(self, p):
        return yy.Heading(4, p[1])

    @_('Heading', 'HeadingU', 'Paragraph', 'Fence')
    def LeafBlock(self, p):
        return p[0]

    @_('Blockquote', 'Ul', 'Ol', 'Tl', 'Fence', 'Admonition', 'Table')
    def ContainerBlock(self, p):
        return p[0]

    @_('TEXT')
    def Span(self, p):
        return yy.Span(p[0])

    @_('CODE_SPAN_OPEN TEXT CODE_SPAN_CLOSE')
    def CodeSpan(self, p):
        return yy.CodeSpan(p[1])

    @_('BOLD_ITALIC_OPEN TEXT BOLD_ITALIC_CLOSE')
    def BoldItalic(self, p):
        return yy.BoldItalic(p[1])

    @_('BOLD_OPEN TEXT BOLD_CLOSE')
    def Bold(self, p):
        return yy.Bold(p[1])

    @_('ITALIC_OPEN TEXT ITALIC_CLOSE')
    def Italic(self, p):
        return yy.Italic(p[1])

    @_('EMOJI')
    def Emoji(self, p):
        return yy.Emoji(p[0])

    @_('LBRACE Inline RBRACE LPAREN TEXT RPAREN')
    def Link(self, p):
        return yy.Link(p[1], p[4])

    @_('BANG LBRACE TEXT RBRACE LPAREN TEXT RPAREN')
    def Image(self, p):
        return yy.Image(p[2], p[5])

    @_('Span', 'CodeSpan', 'Bold', 'Italic', 'BoldItalic', 'Emoji', 'Link', 'Image')
    def Inline(self, p):
        return p[0]

    @_('InlineGroup Inline')
    def InlineGroup(self, p):
        p[0].append(p[1])
        return p[0]

    @_('Inline')
    def InlineGroup(self, p):
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

    @_('InlineGroup TERMINATOR')
    def Text(self, p):
        return yy.Text(p[0])

    # Block quotes
    # Admonition
    @_('BLOCKQUOTE InlineGroup TERMINATOR')
    def Blockquote(self, p):
        return yy.Blockquote(p[1])

    @_('BLOCKQUOTE TERMINATOR Body')
    def Blockquote(self, p):
        return yy.Blockquote(p.Body.children)

    @_('BLOCKQUOTE InlineGroup TERMINATOR Body')
    def Blockquote(self, p):
        return yy.Blockquote(p[1] + p.Body.children)

    '''
    @_('BLOCKQUOTE Text', 'BLOCKQUOTE Body')
    def BlockquoteItem(self, p):
        return p[1]

    @_('BLOCKQUOTE TERMINATOR')
    def BlockquoteItem(self, p):
        return yy.Empty()
    
    @_('Body')
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
    '''
    # Unordered List

    @_('UL Text', 'UL Body')
    def UlItem(self, p):
        return p[1]

    @_('UL TERMINATOR')
    def UlItem(self, p):
        return yy.Empty()

    @_('Body')
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

    @_('OL Text', 'OL Body')
    def OlItem(self, p):
        return p[1]

    @_('OL TERMINATOR')
    def OlItem(self, p):
        return yy.Empty()

    @_('Body')
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

# Task List

    @_('TL Text', 'TL Body')
    def TlItem(self, p):
        checked = 'x' in p[0]
        return yy.TlItem(p[1], checked)

    @_('TL TERMINATOR')
    def TlItem(self, p):
        return yy.Empty()

    @_('Body')
    def TlItem(self, p):
        return p[0]

    @_('TlList TlItem')
    def TlList(self, p):
        p[0].append(p[1])
        return p[0]

    @_('TlItem')
    def TlList(self, p):
        return [p[0]]

    @_('TlList', 'TlList TERMINATOR')
    def Tl(self, p):
        return yy.Tl(p[0])

    # Fence
    @_('FENCE TERMINATOR')
    def Fence(self, p):
        return yy.Fence(p[0])

    @_('FENCE NAME TERMINATOR')
    def Fence(self, p):
        return yy.Fence(p[0], p[1])

    # Admonition
    @_('ADMONITION NAME WS STRING TERMINATOR Body')
    def Admonition(self, p):
        return yy.Admonition(p.Body.children, p.NAME, p.STRING)

    @_('ADMONITION NAME TERMINATOR Body')
    def Admonition(self, p):
        return yy.Admonition(p.Body.children, p.NAME)

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