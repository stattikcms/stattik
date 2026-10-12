class LinkRendererMixin:
    def Link(self, node):
        #self(f'<a href="{node.link}">{node.value}</a>')
        self(f'<a href="{node.link}">')
        self.visit(node.value)
        self('</a>')
    def Image(self, node):
        self(f'<img src="{node.link}" alt="{node.value}"/>')
        
