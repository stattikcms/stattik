import markblocks

from stattik.site import Site

class Markdown:
    
    _instance = None
    @classmethod
    @property
    def instance(cls):
        if cls._instance:
            return cls._instance
        cls._instance = Markdown.produce()
        return cls._instance
    
    def __init__(self):
        self.md = None

    @classmethod
    def produce(cls):
        cls._instance = md = Markdown()

        extensions = [
            'meta',
            'toc',
            'tables',
            'pymdownx.highlight',
            'pymdownx.emoji',
            'pymdownx.superfences',
        ]

        site = Site.get_singleton_sync()
        extensions = extensions + site.markdown_extensions

        extension_configs = {
            'pymdownx.highlight': {
                'auto_title': True
            }
        }

        md.md = markblocks.Markblocks()

        return md
