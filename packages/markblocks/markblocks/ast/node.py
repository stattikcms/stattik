from json import JSONEncoder

from .metanode import MetaNode

TYPE = "type"
VALUE = "value"
LEVEL = "level"
NAME = "name"
CHILDREN = "children"

BODY = "BODY"
VALUE = "value"
ARG = "ARG"
LANG = "lang"
KIND = 'kind'
TITLE = 'title'
LINK = 'link'

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

    def walk(self, fn, reduce):
        return fn(self, reduce(map(lambda child: child.walk(fn, reduce), self.children)))

    def __next__(self):
        for node in self.children:
            yield node

    def toJSON(self):
        return {}

class Empty(Node):
    pass

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

class Link(TextElement):
    def __init__(self, value, link):
        super().__init__(value)
        self.link = link

    def toJSON(self):
        return {TYPE: self.type, VALUE: self.value, LINK: self.link}

class Image(TextElement):
    def __init__(self, value, link):
        super().__init__(value)
        self.link = link

    def toJSON(self):
        return {TYPE: self.type, VALUE: self.value, LINK: self.link}

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

class Blockquote(Block):
    def __init__(self, children):
        super().__init__(children, 'Blockquote')

class Ul(Block):
    def __init__(self, children):
        super().__init__(children, 'Ul')

class Ol(Block):
    def __init__(self, children):
        super().__init__(children, 'Ol')

class TRow(Block):
    def __init__(self, children):
        super().__init__(children, 'TRow')

class THead(Block):
    def __init__(self, children, separator):
        super().__init__(children, 'THead')
        self.separator = separator

class TBody(Block):
    def __init__(self, children):
        super().__init__(children, 'TBody')

class Table(Block):
    def __init__(self, children):
        super().__init__(children, 'Table')

class Fence(Node):
    def __init__(self, value, lang=None):
        super().__init__()
        self.value = value
        self.lang = lang

    def toJSON(self):
        return {TYPE: self.type, VALUE: self.value, LANG: self.lang}

class Admonition(Block):
    def __init__(self, children, kind, title=None):
        super().__init__(children, 'Admonition')
        self.kind = kind
        self.title = title

    def toJSON(self):
        return {TYPE: self.type, KIND: self.kind, TITLE: self.title, CHILDREN: self.children}


class Emoji(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def toJSON(self):
        return {TYPE: self.type, NAME: self.name}
