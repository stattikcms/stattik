from stattik.architect import builders
from stattik.architect.builders import MarkdownBuilder, Paginator

from .project import ProjectsBuilder

builders = [
    MarkdownBuilder,
    ProjectsBuilder,
    Paginator
]