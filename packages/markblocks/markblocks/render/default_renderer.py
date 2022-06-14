from .renderer import Renderer
from .fence_renderer_mixin import FenceRendererMixin
from .admonition_renderer_mixin import AdmonitionRendererMixin
from .emoji_renderer_mixin import EmojiRendererMixin
from .link_renderer_mixin import LinkRendererMixin
from .table_renderer_mixin import TableRendererMixin


class DefaultRenderer(Renderer, FenceRendererMixin, AdmonitionRendererMixin, EmojiRendererMixin, LinkRendererMixin, TableRendererMixin):

    Document = Renderer.visits

    Block = Renderer.visits

    def Text(self, node):
        with self.inlined:
            self(self.indentation())
            for child in node.children:
                self.visit(child)

    def Span(self, node):
        self(node.value)

    def Paragraph(self, node):
        self('<p>')
        with self.scope:
            self.visits(node)
        self('</p>')

    def Heading(self, node):
        self(f"<h{node.level}>")
        with self.scope:
            self.visits(node)
        self(f"</h{node.level}>")

    def Italic(self, node):
        self('<em>')
        self.value_(node)
        self('</em>')

    def Bold(self, node):
        self('<strong>')
        self.value_(node)
        self('</strong>')

    def BoldItalic(self, node):
        self('<strong><em>')
        self.value_(node)
        self('</em></strong>')

    def Ul(self, node):
        self('<ul>')
        with self.scope:
            for child in node.children:
                self('<li>')
                with self.scope:
                    self.visit(child)
                self('</li>')
        self('</ul>')

    def Ol(self, node):
        self('<ol>')
        with self.scope:
            for child in node.children:
                self('<li>')
                with self.scope:
                    self.visit(child)
                self('</li>')
        self('</ol>')

    def Blockquote(self, node):
        self('<blockquote>')
        with self.indented:
            self.visits(node)
        self('</blockquote>')
