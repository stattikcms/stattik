from sqlalchemy import Column, Integer, ForeignKey

from .page import Page, PageRepository

class Post(Page):
    id = Column(Integer, ForeignKey('Page.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'Post',
    }

class PostRepository(PageRepository):
    Model = Post
