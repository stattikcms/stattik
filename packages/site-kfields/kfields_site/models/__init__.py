import stattik.database
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

def create_database():
    return stattik.database.create_database(repositories)
