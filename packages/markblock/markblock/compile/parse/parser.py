import sys
import sly

from markblock.compile.lex.lexer import Lexer
import markblock.compile.ast.node  as yy

class Parser(sly.Parser):
    tokens = Lexer.tokens
    def __init__(self):
        super().__init__()

    def error(self, token):
        '''
        Default error handling function.  This may be subclassed.
        '''
        if token:
            lineno = getattr(token, 'lineno', 0)
            if lineno:
                sys.stderr.write(f'sly: Syntax error at line {lineno}, token={token.type}\n')
            else:
                sys.stderr.write(f'sly: Syntax error, token={token.type}')
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

    @_('Expression')
    def ExprList(self, p):
        return [p.Expression]

    @_('Statement', 'Expression')
    def Line(self, p):
        return p[0]

    @_('TERMINATOR')
    def Expression(self, p):
        return p[0]

    @_('TextElementList TERMINATOR H1U TERMINATOR')
    def HeadingU(self, p):
        return yy.Heading(1, p[0])

    @_('TextElementList TERMINATOR H2U TERMINATOR')
    def HeadingU(self, p):
        return yy.Heading(2, p[0])

    @_('H1 TextElementList TERMINATOR')
    def Heading(self, p):
        return yy.Heading(len(p[0]), p[1])

    @_('H2 TextElementList TERMINATOR')
    def Heading(self, p):
        return yy.Heading(len(p[0]), p[1])

    @_('H3 TextElementList TERMINATOR')
    def Heading(self, p):
        return yy.Heading(len(p[0]), p[1])

    @_('TAG Expression')
    def Tag(self, p):
        return yy.ImportStmt(p.Expression)

    @_('HeadingU', 'Paragraph', 'BlockQuote')
    def Statement(self, p):
        return p[0]

    @_('Tag')
    def Statement(self, p):
        return p[0]

    @_('Heading')
    def Expression(self, p):
        return p[0]

    @_('SPAN')
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

    @_('Span', 'Bold', 'Italic', 'BoldItalic')
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

    @_('BLOCKQUOTE Text')
    def BlockQuoteItem(self, p):
        return p[1]

    @_('BLOCKQUOTE Block')
    def BlockQuoteItem(self, p):
        return p[1]

    @_('BLOCKQUOTE TERMINATOR')
    def BlockQuoteItem(self, p):
        return None

    @_('Block')
    def BlockQuoteItem(self, p):
        return p[0]


    @_('BlockQuoteList BlockQuoteItem')
    def BlockQuoteList(self, p):
        p[0].append(p[1])
        return p[0]

    @_('BlockQuoteItem')
    def BlockQuoteList(self, p):
        return [p[0]]

    @_('BlockQuoteList')
    def BlockQuote(self, p):
        return yy.BlockQuote(p[0])

    @_('BlockQuoteList TERMINATOR')
    def BlockQuote(self, p):
        return yy.BlockQuote(p[0])
