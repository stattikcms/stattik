import markblocks

from stattik.site import Site

class Markdown:
    
    _instance = None
    @classmethod
    @property
    def instance(self):
        if self._instance:
            return self._instance
        self._instance = Markdown.produce()
        return self._instance
    
    def __init__(self):
        self.md = None

    @classmethod
    def produce(self):
        self._instance = md = Markdown()

        extensions = [
            'meta',
            'toc',
            'tables',
            'pymdownx.highlight',
            'pymdownx.emoji',
            'pymdownx.superfences',
        ]

        extensions = extensions + Site.instance.markdown_extensions

        extension_configs = {
            'pymdownx.highlight': {
                'auto_title': True
            }
        }

        md.md = markblocks.Markblocks()

        return md
