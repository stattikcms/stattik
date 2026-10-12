from json import JSONEncoder

from .metanode import MetaNode

KIND = "kind"
VALUE = "value"
LEVEL = "level"
NAME = "name"
CHILDREN = "children"

LANG = "lang"
FLAVOR = 'flavor'
TITLE = 'title'
LINK = 'link'

_terms = {}
_types = {}


class AstEncoder(JSONEncoder):
    def default(self, o):
        return o.toJSON()


class Node(object, metaclass=MetaNode):
    @property
    def kind(self):
        return self.__class__.__name__

    def __init__(self):
        super().__init__()
        self.children = [None] * self.nodeCount
        self.scope = None
        self.binding = None

    def add(self, child):
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
        return { KIND: self.kind }

class Empty(Node):
    pass


class Property(Node):
    def __init__(self, name, val):
        super.__init__()
        self.name = name
        self.value = val

    def toJSON(self):
        return {KIND: self.kind, NAME: self.name, VALUE: self.value}


class Properties(Node):
    def __init__(self, child):
        super().__init__()
        self.add(child)

class Group(Node):
    def __init__(self, children):
        super().__init__()
        self.children = children

    def toJSON(self):
        return {KIND: self.kind, CHILDREN: self.children}

class InlineGroup(Group):
    def __init__(self, children):
        super().__init__(children)

class Block(Group):
    def __init__(self, children):
        super().__init__(children)

#
# Document
#
class Document(Block):
    def __init__(self, children):
        super().__init__(children)

class Paragraph(Block):
    def __init__(self, children):
        super().__init__(children)

class Inline(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def toJSON(self):
        return {KIND: self.kind, VALUE: self.value}

class Link(Inline):
    def __init__(self, value, link):
        super().__init__(value)
        self.link = link

    def toJSON(self):
        return {KIND: self.kind, VALUE: self.value, LINK: self.link}

class Image(Inline):
    def __init__(self, value, link):
        super().__init__(value)
        self.link = link

    def toJSON(self):
        return {KIND: self.kind, VALUE: self.value, LINK: self.link}

class Text(Inline):
    pass

class CodeSpan(Inline):
    pass

class Bold(Inline):
    pass

class Italic(Inline):
    pass

class BoldItalic(Inline):
    pass

class Heading(Block):
    def __init__(self, level, children):
        super().__init__(children)
        self.level = level

    def toJSON(self):
        return {KIND: self.kind, LEVEL: self.level, CHILDREN: self.children}

class Blockquote(Block):
    def __init__(self, children):
        super().__init__(children)

class Ul(Block):
    def __init__(self, children):
        super().__init__(children)

class Ol(Block):
    def __init__(self, children):
        super().__init__(children)

class Tl(Block):
    def __init__(self, children):
        super().__init__(children)

class TlItem(Node):
    def __init__(self, value, checked=False):
        super().__init__()
        self.value = value
        self.checked = checked

class TRow(Block):
    def __init__(self, children):
        super().__init__(children)

class THead(Block):
    def __init__(self, children, separator):
        super().__init__(children)
        self.separator = separator

class TBody(Block):
    def __init__(self, children):
        super().__init__(children)

class Table(Block):
    def __init__(self, children):
        super().__init__(children)

class Fence(Node):
    def __init__(self, value, lang=None):
        super().__init__()
        self.value = value
        self.lang = lang

    def toJSON(self):
        return {KIND: self.kind, VALUE: self.value, LANG: self.lang}

class Admonition(Block):
    def __init__(self, children, flavor, title=None):
        super().__init__(children)
        self.flavor = flavor
        self.title = title

    def toJSON(self):
        return {KIND: self.kind, FLAVOR: self.flavor, TITLE: self.title, CHILDREN: self.children}


class Emoji(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def toJSON(self):
        return {KIND: self.kind, NAME: self.name}
