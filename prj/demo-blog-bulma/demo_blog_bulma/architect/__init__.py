from stattik import architect

from .builders import builders

def create_architect():
    return architect.create_architect(builders)
