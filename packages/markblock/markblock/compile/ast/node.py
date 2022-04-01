from json import JSONEncoder

from .metanode import MetaNode

TYPE = "type"
VALUE = "value"
LEVEL = "level"
NAME = "name"
CHILDREN = "children"
SUBJ = "SUBJ"
VERB = "VERB"
OBJ = "OBJ"
XTRA = "XTRA"
TRIGGER = "TRIGGER"
BODY = "BODY"
FLAVOR = "FLAVOR"
BINDING = "BINDING"
VALUE = "value"
ARG = "ARG"

_terms = {}
_types = {}


class AstEncoder(JSONEncoder):
    def default(self, o):
        return o.toJSON()


class Node(object, metaclass=MetaNode):
    def __init__(self, type=None):
        super().__init__()
        self.type = type or self.__class__.__name__
        self.children = [None] * self.nodeCount
        self.scope = None
        self.binding = None

    def add(self, child):
        # child.parent = self
        return self.children.append(child)

    def remove(self, child):
        index = self.children.indexOf(child)
        if index > -1:
            return self.children.splice(index, 1)

    def walk(self, fn):
        fn.apply(self)
        return self.children.map(lambda child: child.walk(fn))

    def __next__(self):
        for node in self.CHILDREN:
            yield node


class Array(Node):
    def __init__(self, children):
        super().__init__()
        self.children = children

    def toJSON(self):
        return {TYPE: self.type, TYPE: self.type, CHILDREN: self.children}


class Property(Node):
    def __init__(self, name, val):
        super.__init__()
        self.name = name
        self.value = val

    def toJSON(self):
        return {TYPE: self.type, NAME: self.name, VALUE: self.value}


class Properties(Node):
    def __init__(self, child):
        super().__init__()
        self.add(child)


class Variable(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.info = None

    def toJSON(self):
        return {TYPE: self.type, NAME: self.name, TYPE: self.type, INFO: self.info}


class Term(Node):
    def __init__(self, name, type="Term"):
        super().__init__(type)
        self.name = name

    def toJSON(self):
        return {TYPE: self.type, NAME: self.name, TYPE: self.type}


def term_(name):
    term = _terms.get(name)
    if not term:
        term = Term(name)
        _terms[name] = term
    return term


class Type(Term):
    def __init__(self, name):
        super().__init__(name, "Type")
        self.builtin = False

    def toJSON(self):
        return {TYPE: self.type, NAME: self.name}


def type_(name):
    t = _types.get(name)
    if not t:
        t = Type(name)
        _types[name] = t
    return t


def builtin_(name):
    t = type_(name)
    t.builtin = True
    return t


_Goal = builtin_("Goal")
_Achieve = builtin_("Achieve")
_Believe = builtin_("Believe")
#


class Literal(Node):
    def __init__(self, value):
        super().__init__("Literal")
        self.value = value

    def toJSON(self):
        return {TYPE: self.type, VALUE: self.value}


_null = Literal("null")
#


class ExprList(Node):
    def __init__(self, children, type="ExprList"):
        super().__init__(type)
        self.children = children

class Block(ExprList):
    def __init__(self, children, type="Block"):
        super().__init__(children, type)

    def toJSON(self):
        return {TYPE: self.type, CHILDREN: self.children}


#
# Document
#
class Document(Block):
    def __init__(self, children):
        super().__init__(children, "Document")


class Text(Block):
    def __init__(self, children):
        super().__init__(children, 'Text')

class Paragraph(Block):
    def __init__(self, children):
        super().__init__(children, 'Paragraph')

class TextElement(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def toJSON(self):
        return {TYPE: self.type, VALUE: self.value}

class Span(TextElement):
    pass

class Bold(TextElement):
    pass

class Italic(TextElement):
    pass

class BoldItalic(TextElement):
    pass

class Heading(Block):
    def __init__(self, level, children):
        super().__init__(children, 'Heading')
        self.level = level

    def toJSON(self):
        return {TYPE: self.type, LEVEL: self.level, CHILDREN: self.children}

class BlockQuote(Block):
    def __init__(self, children):
        super().__init__(children, 'BlockQuote')

class Ul(Block):
    def __init__(self, children):
        super().__init__(children, 'Ul')

class Ol(Block):
    def __init__(self, children):
        super().__init__(children, 'Ol')

class Snippet(Node):
    def __init__(self, t):
        super().__init__()
        t = t.slice(1)
        t = t.trim()
        self.text = t

    def toJSON(self):
        return {TYPE: self.type, text: self.text}


class Code(Node):
    def __init__(self, t):
        super().__init__()
        t = t.substring(1, t.length - 1)
        t = t.trim()
        self.text = t

    def toJSON(self):
        return {TYPE: self.type, text: self.text}

class Sentence(Node):
    Node.node("clause")
    Node.node("list")

    def __init__(self, clause, arr):
        super().__init__()
        self.clause = clause
        self.list = arr

    def toJSON(self):
        return {TYPE: self.type, TYPE: self.type, clause: self.clause, LIST: self.list}


class Clause(Node):
    Node.node("subj")
    Node.node("verb")
    Node.node("obj")

    def __init__(self, subj, verb, obj, t=type_("Believe")):
        super().__init__()
        self.subj = subj
        self.verb = verb
        self.obj = obj
        self.type = t
        self.xtra = None
        self.binding = None

    def toJSON(self):
        return {
            TYPE: self.type,
            TYPE: self.type,
            SUBJ: self.subj,
            VERB: self.verb,
            OBJ: self.obj,
            XTRA: self.xtra,
        }


class Trigger(Node):
    def __init__(self, arg):
        super().__init__()
        msg = None
        if isinstance(arg, Clause):
            clause = arg
            if not clause.subj:
                clause.type = type_("Achieve")
                msg = Attempt(clause)
            else:
                clause.type = type_("Believe")
                msg = Assert(clause)
        else:
            msg = arg

        self.flavor = msg.type
        expr = msg.arg
        self.type = expr.type
        if isinstance(expr, Clause):
            self.subj = expr.subj
            self.verb = expr.verb
            self.obj = expr.obj
            self.xtra = expr.xtra
            self.binding = expr.binding
        elif isinstance(expr, Variable):
            self.binding = expr

    def toJSON(self):
        return {
            TYPE: self.type,
            FLAVOR: self.flavor,
            TYPE: self.type,
            SUBJ: self.subj,
            VERB: self.verb,
            OBJ: self.obj,
            XTRA: self.xtra,
            BINDING: self.binding,
        }


class UnaryExpr(Node):
    Node.node("arg")

    def __init__(self, arg, type="UnaryExpr"):
        super().__init__(type)
        self.arg = arg

    def toJSON(self):
        return {TYPE: self.type, ARG: self.arg}


class PrefixExpr(UnaryExpr):
    def __init__(self, arg, type="PrefixExpr"):
        super().__init__(arg, type)


#
# Messages
#
_Propose = builtin_("Propose")
_Attempt = builtin_("Attempt")
_Assert = builtin_("Assert")
_Retract = builtin_("Retract")


class Message(PrefixExpr):
    def __init__(self, arg, t=_Assert):
        super().__init__(arg, "Message")

        self.type = t
        if isinstance(arg, Clause):
            clause = arg
            if not clause.subj:
                clause.type = type_("Achieve")

    def toJSON(self):
        return {TYPE: self.type, TYPE: self.type, ARG: self.arg}


class Propose(Message):
    def __init__(self, arg):
        super().__init__(arg, _Propose)


class Attempt(Message):
    def __init__(self, arg):
        super().__init__(arg, _Attempt)


class Assert(Message):
    def __init__(self, arg):
        super().__init__(arg, _Assert)


class Retract(Message):
    def __init__(self, arg):
        super(arg, _Retract)


class PostfixExpr(UnaryExpr):
    def __init__(self, arg, type="PostfixExpr"):
        super().__init__(arg, type)


class BinaryExpr(Node):
    Node.node("left")
    Node.node("right")

    def __init__(self, left, right, type="BinaryExpr"):
        super().__init__(type)
        self.left = left
        self.right = right

    def toJSON(self):
        return {TYPE: self.type, op: self.op, left: self.left, right: self.right}


class Contextualize(Node):
    Node.node("left")
    Node.node("right")

    def __init__(self, left, right):
        super().__init__("Contextualize")
        self.left = left
        self.right = right

    def toJSON(self):
        return {TYPE: self.type, left: self.left, right: self.right}


class Statement(Node):
    def __init__(self, type="Statement"):
        super().__init__(type)

    def toJSON(self):
        return {TYPE: self.type}


class Def(Statement):
    Node.node("trigger")
    Node.node("body")

    def __init__(self, trigger, body, type="Def"):
        super().__init__(type)
        self.trigger = trigger
        self.body = body

    def toJSON(self):
        return {TYPE: self.type, TRIGGER: self.trigger, BODY: self.body}


class Sig(Def):
    def __init__(self, trigger, body):
        super(trigger, body, "Sig")


class ImportStmt(Statement):
    def __init__(self, expr):
        super().__init__("ImportStmt")
        self.expr = expr

    def toJSON(self):
        return {TYPE: self.type, expr: self.expr}


#
class Query(Statement):
    Node.node("lhs")
    Node.node("rhs")

    def __init__(self, lhs, rhs):
        super().__init__("Query")
        self.lhs = lhs
        self.rhs = rhs

    def toJSON(self):
        return {TYPE: self.type, lhs: self.lhs, rhs: self.rhs}


class Condition(Node):
    Node.node("expr")

    def __init__(self, expr, type="Condition"):
        super().__init__(type)
        self.expr = expr

    def toJSON(self):
        return {TYPE: self.type, expr: self.expr}


class QClause(Condition):
    def __init__(self, expr):
        super.__init__(expr, "QClause")


class QNegClause(Condition):
    def __init__(expr):
        super().__init__(expr, "QNegClause")


class QFilter(Condition):
    def __init__(self, expr):
        super().__init__(expr, "QFilter")


class Lhs(ExprList):
    def __init__(self, child, type):
        super().__init__(child, "Lhs")


class Rhs(Block):
    def __init__(self, child, type):
        super(child, "Rhs")


#
# Actions
#
class Actions(Node):
    def __init__(self, body, type):
        super().__init__(self, type)
        self.body = body

    def toJSON(self):
        return {TYPE: self.type, BODY: self.body}


#
class Action(Node):
    def __init__(self, expr, type="Action"):
        super().__init__(type)
        self.expr = expr

    def toJSON(self):
        return {TYPE: self.type, expr: self.expr}
