from stattik.architect import builders
from stattik.architect.builders import MarkdownBuilder

from .project import ProjectsBuilder

builders = [
    MarkdownBuilder,
    ProjectsBuilder,
]