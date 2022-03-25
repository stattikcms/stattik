from sqlalchemy import Column, Integer, ForeignKey

from .page import Page, PageRepository

class Landing(Page):
    id = Column(Integer, ForeignKey('Page.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'Landing',
    }

class LandingRepository(PageRepository):
    Model = Landing
