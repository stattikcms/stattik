import stattik.database
from stattik.repositories.page import PageRepository
from .landing import LandingRepository
from .post import PostRepository

repositories = [
    PageRepository,
    LandingRepository,
    PostRepository,
]

def create_database():
    return stattik.database.create_database(repositories)
