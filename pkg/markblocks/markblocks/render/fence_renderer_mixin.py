from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class FenceRendererMixin:
    def Fence(self, node):
        if not node.lang:
            self('<pre><code>')
            self.value_(node)
            self('</code></pre>')
            return

        lexer = get_lexer_by_name(node.lang)
        self(highlight(node.value, lexer, HtmlFormatter()))
        
