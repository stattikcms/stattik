from typing import TypedDict

class PostShape(TypedDict):
    title: bool

class AuthorShape(TypedDict):
    name: bool
    posts: PostShape

def test():
    shape: AuthorShape = AuthorShape(
        posts = PostShape(title=True)
    )

    
'''
from typing import NamedTuple

class PostShape(NamedTuple):
    title: bool

class AuthorShape(NamedTuple):
    name: bool
    posts: PostShape

def test():
    shape: AuthorShape = {

    }
'''