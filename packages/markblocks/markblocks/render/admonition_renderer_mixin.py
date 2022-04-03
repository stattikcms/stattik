class AdmonitionRendererMixin:
    def Admonition(self, node):
        self(f'<div class="admonition {node.kind}">')
        if node.title:
            title = node.title
        else:
            title = node.kind.capitalize()

        with self.indented:
            self(f'<p class="admonition-title">{title}</p>')
            self.visits(node)

        self('</div>')
