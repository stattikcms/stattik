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


    @_('Module')
    def File(self, p):
        return p.Module

    @_('Body')
    def Module(self, p):
        return yy.Module(p.Body)

    @_('INDENT DEDENT')
    def Block(self, p):
        return yy.Block()

    @_('INDENT Body DEDENT')
    def Block(self, p):
        return p.Body

    @_('Line')
    def Body(self, p):
        return yy.Block(p.Line)

    @_('Body TERMINATOR Line')
    def Body(self, p):
        p.Body.add(p.Line)
        return p.Body

    @_('Body TERMINATOR')
    def Body(self, p):
        return p.Body

    @_('Expression')
    def ExprList(self, p):
        return [p.Expression]

    @_('ExprList TERMINATOR Expression')
    def ExprList(self, p):
        return p.ExprList.append(p.Expression)

    @_('ExprList TERMINATOR')
    def ExprList(self, p):
        return p.ExprList

    @_('Statement', 'Expression')
    def Line(self, p):
        return p[0]

    @_('Import', 'Def', 'Sig', 'Where', 'Return', 'Halt')
    def Statement(self, p):
        return p[0]

    @_('Expression')
    def Action(self, p):
        return yy.Action(p.Expression)

    @_('IMPORT Expression')
    def Import(self, p):
        return yy.ImportStmt(p.Expression)

    @_('Expression')
    def Trigger(self, p):
        return yy.Trigger(p.Expression)

    @_('DEF LPAR Trigger RPAR Block')
    def Def(self, p):
        return yy.Def(p.Trigger, p.Block)

    @_('SIG LPAR Trigger RPAR Block')
    def Sig(self, p):
        return yy.Sig(p.Trigger, p.Block)

    @_('QClause', 'QNegClause', 'QFilter')
    def Condition(self, p):
        return p[0]

    @_('Clause')
    def QClause(self, p):
        return yy.QClause(p.Clause)

    @_('NegClause')
    def QNegClause(self, p):
        return yy.QNegClause(p.NegClause)

    @_('Expression')
    def QFilter(self, p):
        return yy.QFilter(p.Expression)

    @_('WHERE INDENT Lhs DEDENT Rhs')
    def Where(self, p):
        return yy.Query(p.Lhs, p.Rhs)

    @_('Condition')
    def Lhs(self, p):
        return yy.Lhs(p.Condition)

    @_('Lhs TERMINATOR Condition')
    def Lhs(self, p):
        p.Lhs.add(p.Condition)
        return p.Lhs

    @_('Lhs TERMINATOR')
    def Lhs(self, p):
        return p.Lhs

    @_('WhereTrue')
    def Rhs(self, p):
        return yy.Rhs(p.WhereTrue)

    @_('Rhs WhereFalse')
    def Rhs(self, p):
        p.Rhs.add(p.WhereFalse)
        return p.Rhs

    @_('Rhs WhereAllTrue')
    def Rhs(self, p):
        p.Rhs.add(p.WhereAllTrue)
        return p.Rhs

    @_('Rhs WhereAllFalse')
    def Rhs(self, p):
        p.Rhs.add(p.WhereAllFalse)
        return p.Rhs

    @_('LONGARROW Block')
    def WhereTrue(self, p):
        return yy.Actions(p.Block, p.LONGARROW)

    @_('NARROW Block')
    def WhereFalse(self, p):
        return yy.Actions(p.Block, p.NARROW)

    @_('LONGFATARROW Block')
    def WhereAllTrue(self, p):
        return yy.Actions(p.Block, p.LONGFATARROW)

    @_('NFATARROW Block')
    def WhereAllFalse(self, p):
        return yy.Actions(p.Block, p.LONGFATARROW)

    @_('ParExpr', 'PrefixExpr', 'PostfixExpr', 'BinaryExpr', 'Paragraph', 'Terminal')
    def Expression(self, p):
        return p[0]

    @_('Literal', 'Variable', 'Term', 'Snippet', 'Code')
    def Terminal(self, p):
        return p[0]

    @_('STRING', 'NUMBER', 'TRUE', 'FALSE')
    def Literal(self, p):
        return p[0]

    @_('VARIABLE')
    def Variable(self, p):
        return yy.Variable(p.VARIABLE.slice(1))

    @_('VERB')
    def Verb(self, p):
        return yy.term_(p.VERB)

    @_('NOUN')
    def Term(self, p):
        return yy.term_(p.NOUN)

    @_('SNIPPET')
    def Snippet(self, p):
        return yy.Snippet(p.SNIPPET)

    @_('CODE')
    def Code(self, p):
        return yy.Code(p.CODE)

    @_('Sentence')
    def Paragraph(self, p):
        return p.Sentence

    @_('Expression DCOLON INDENT ExprList DEDENT')
    def Paragraph(self, p):
        return yy.Paragraph(p.Expression, p.ExprList)

    @_('Sentence')
    def SentenceList(self, p):
        return p.Sentence

    @_('SentenceList TERMINATOR Sentence')
    def SentenceList(self, p):
        p.SentenceList.append(p.Sentence)
        return p.SentenceList

    @_('SentenceList TERMINATOR')
    def SentenceList(self, p):
        return p.SentenceList

    @_('ClauseExpr')
    def Sentence(self, p):
        return p.ClauseExpr

    @_('ClauseExpr AMP AmpList')
    def Sentence(self, p):
        return yy.Sentence(p.ClauseExpr, p.AmpList)

    @_('Expression')
    def AmpList(self, p):
        return p.Expression

    @_('AmpList AMP Expression')
    def AmpList(self, p):
        p.AmpList.append(p.Expression)
        return p.AmpList

    @_('Clause', 'BindExpr')
    def ClauseExpr(self, p):
        return p[0]

    @_('Clause ARROW Variable')
    def BindExpr(self, p):
        p.Clause.binding = p.Variable
        return p.Clause

    @_('NotOp Clause')
    def NegClause(self, p):
        p.Clause.negated = True
        return p.Clause

    @_('SimpleClause')
    def Clause(self, p):
        return p.SimpleClause

    @_('SimpleClause Properties')
    def Clause(self, p):
        p.SimpleClause.xtra = Properties
        return p.SimpleClause

    @_('Expression Verb ObjExpr')
    def SimpleClause(self, p):
        return yy.Clause(p.Expression, p.Verb, p.ObjExpr)

    @_('Expression Verb')
    def SimpleClause(self, p):
        return yy.Clause(p.Expression, p.Verb, yy._null)

    @_('Verb ObjExpr')
    def SimpleClause(self, p):
        return yy.Clause(yy._null, p.Verb, p.ObjExpr)

    @_('Verb')
    def SimpleClause(self, p):
        return yy.Clause(yy._null, p.Verb, yy._null)

    @_('Expression')
    def ObjExpr(self, p):
        #return p.CommaList if len(p.CommaList) < 1 else yy.Array(p.CommaList)
        return p.Expression

    @_('CommaList')
    def ObjExpr(self, p):
        #return p.CommaList if len(p.CommaList) < 1 else yy.Array(p.CommaList)
        return yy.Array(p.CommaList)  if isinstance(p.CommaList, list) else p.CommaList

    @_('Expression')
    def CommaList(self, p):
        return [p.Expression]

    @_('CommaList COMMA Expression')
    def CommaList(self, p):
        p.CommaList.append(p.Expression)
        return p.CommaList

    @_('TYPE')
    def TypeName(self, p):
        return p.TYPE.slice(0, -1)

    @_('POSTTYPE')
    def PostTypeName(self, p):
        return p.POSTTYPE.slice(1)

    @_('PROPERTY')
    def PropertyName(self, p):
        return p.PROPERTY.slice(0, -1)

    @_('PropertyName')
    def Property(self, p):
        return yy.Property(p.PropertyName)

    @_('PropertyName Expression')
    def Property(self, p):
        return yy.Property(p.PropertyName, p.Expression)

    @_('Property')
    def Properties(self, p):
        return yy.Properties(p.Property)

    @_('Properties Property')
    def Properties(self, p):
        p.Properties.add(p.Property)
        return p.Properties

    @_('LPAR RPAR')
    def ParExpr(self, p):
        return None

    @_('LPAR Expression RPAR')
    def ParExpr(self, p):
        return p.Expression

    @_('Typed', 'Not', 'Slash', 'Message')
    def PrefixExpr(self, p):
        return p[0]

    @_('TypeName Expression')
    def Typed(self, p):
        p.Expression.type = yy.type_(p.TypeName)
        return p.Expression

    @_('BANG', 'NOT')
    def NotOp(self, p):
        return p[0]

    @_('NotOp Expression')
    def Not(self, p):
        return yy.PrefixExpr(p.Expression, p.NotOp)

    @_('SLASH Expression')
    def Slash(self, p):
        p.Expression.slash = True
        return p.Expression

    @_('Propose', 'Attempt', 'Assert', 'Retract', 'Modify')
    def Message(self, p):
        return p[0]

    @_('STAR Expression')
    def Propose(self, p):
        return yy.Propose(p.Expression)

    @_('AT Expression')
    def Attempt(self, p):
        return yy.Attempt(p.Expression)

    @_('PLUS Expression')
    def Assert(self, p):
        return yy.Assert(p.Expression)

    @_('MINUS Expression')
    def Retract(self, p):
        return yy.Retract(p.Expression)

    @_('MINUSPLUS Expression')
    def Modify(self, p):
        return yy.Modify(p.Expression)

    @_('PostTyped', 'Achieve')
    def PostfixExpr(self, p):
        return p[0]

    @_('Expression PostTypeName')
    def PostTyped(self, p):
        p.Expression.type = yy.type_(p.PostTypeName)
        return p.Expression

    @_('Expression BANG')
    def Achieve(self, p):
        return yy.PostfixExpr(p.Expression, p.BANG)

    @_('ContextExpr', 'InjectExpr', 'TypeOfExpr', 'AssignExpr', 'EqualExpr', 'NotEqualExpr', 'InstanceOfExpr')
    def BinaryExpr(self, p):
        return p[0]

    @_('Expression LTCOLON INDENT ExprList DEDENT')
    def ContextExpr(self, p):
        return yy.BinaryExpr(p.Expression, p.ExprList, p.LTCOLON)

    @_('Expression LTLTCOLON Expression')
    def InjectExpr(self, p):
        return yy.BinaryExpr(p[0], p[2], p.LTLTCOLON)

    @_('Expression CARET Expression')
    def TypeOfExpr(self, p):
        return yy.BinaryExpr(p[0], p[2], p.CARET)

    @_('Expression EQ Expression')
    def AssignExpr(self, p):
        return yy.BinaryExpr(p[0], p[2], p.EQ)

    @_('Expression EQEQ Expression')
    def EqualExpr(self, p):
        return yy.BinaryExpr(p[0], p[2], p.EQEQEQ)

    @_('Expression EQEQ Expression')
    def NotEqualExpr(self, p):
        return yy.BinaryExpr(p[0], p[2], p.BANGEQ)

    @_('Expression INSTANCEOF Expression')
    def InstanceOfExpr(self, p):
        return yy.BinaryExpr(p[0], p[2], p.INSTANCEOF)

    @_('RETURN Expression')
    def Return(self, p):
        return yy.Return(p.Expression)

    @_('RETURN')
    def Return(self, p):
        return yy.Return()

    @_('HALT Expression')
    def Halt(self, p):
        return yy.Halt(p.Expression)

    @_('HALT')
    def Halt(self, p):
        return yy.Halt()
