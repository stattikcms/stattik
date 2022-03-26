from stattik.models.page import PageRepository
from .landing import LandingRepository
from .post import PostRepository
from .project import ProjectRepository

repositories = [
    PageRepository,
    LandingRepository,
    PostRepository,
    ProjectRepository,
]