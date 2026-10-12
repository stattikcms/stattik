import yaml
import frontmatter

from stattik.data.loader import Loader

class YAMLHandler(frontmatter.default_handlers.YAMLHandler):

    def load(self, fm, **kwargs):
        """
        Parse YAML front matter. This uses yaml.SafeLoader by default.
        """
        kwargs.setdefault("Loader", Loader)
        return yaml.load(fm, **kwargs)

def load(fm):
    return frontmatter.load(fm, handler=YAMLHandler())

def loads(text):
    return frontmatter.loads(text, handler=YAMLHandler())