class TableRendererMixin:
    def TRow(self, node):
        self('<tr>')
        with self.scope:
            for child in node.children:
                self('<td>')
                with self.scope:
                    self.visit(child)
                self('</td>')
        self('</tr>')

    def THead(self, node):
        self('<thead><tr>')
        with self.scope:
            for child in node.children:
                self('<th>')
                with self.scope:
                    self.visit(child)
                self('</th>')
        self('</tr></thead>')

    def TBody(self, node):
        self('<tbody>')
        with self.scope:
            for child in node.children:
                with self.scope:
                    self.visit(child)
        self('</tbody>')

    def Table(self, node):
        self('<table>')
        with self.scope:
            for child in node.children:
                with self.scope:
                    self.visit(child)
        self('</table>')
