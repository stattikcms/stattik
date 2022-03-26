from sqlalchemy import Column, Integer, ForeignKey

from stattik.models.page import Page, PageRepository

class Project(Page):
    id = Column(Integer, ForeignKey('Page.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'Project',
    }

class ProjectRepository(PageRepository):
    Model = Project
