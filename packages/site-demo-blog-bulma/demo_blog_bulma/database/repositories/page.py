from typing import Optional
from datetime import datetime
import json

from sqlalchemy import Column, Integer, JSON, String, DateTime, Text, event, func
from sqlalchemy.future import select

from stattik.database import Repository
from stattik.model import Model
from stattik.data import Data

import sqlalchemy.types as types
from pathlib import Path

class PathType(types.TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return Path(value)

class Page(Model):
    def __init__(self, data={}) -> None:
        self.inject(data)

    def inject(self, data):
        for key in data:
            setattr(self, key, data[key])

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    data = Column(JSON)

    title = Column(String(50))
    date = Column(DateTime, index=True, default=datetime.utcnow())
    stars = Column(Integer, index=True)
    
    description = Column(String(50))
    cover = Column(String(50))
    slug = Column(String(50))

    path = Column(PathType(50))
    url = Column(PathType(50))
    content = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity':'Page',
        'polymorphic_on':type
    }
'''
@event.listens_for(Page, "load")
def _inject_data(target, context):
    print(context.data)
    target.inject(context.data)
'''

#event.listen(Page, 'load', _inject_data)

class PageData(Data):
    id: int
    type: str
    title: str
    date: datetime
    description: str
    cover: str
    slug: str

class PageInput(Data):
    type: str
    title: Optional[str]
    date: Optional[datetime]
    description: Optional[str]
    cover: Optional[str]
    slug: Optional[str]

class PageRepository(Repository):
    Input = PageInput
    Data = PageData
    Model = Page

    async def add(self, page):
        session = self.Session()
        session.add(page)
        await session.flush()

    async def create(self, data):
        session = self.Session()
        page = self.Model(**dict(data))
        session.add(page)
        await session.flush()

    async def all(self):
        session = self.Session()
        q = await session.execute(select(self.Model).order_by(self.Model.id))
        return q.scalars().all()

    async def count(self):
        session = self.Session()
        q = await session.execute(select(func.count()).select_from(select(self.Model).subquery()))
        count = q.scalars().one()
        return count

    async def slice(self, start, stop):
        session = self.Session()
        q = await session.execute(select(self.Model).order_by(self.Model.id).slice(start, stop))
        return q.scalars().all()

    async def latest(self, start, stop):
        session = self.Session()
        q = await session.execute(select(self.Model).order_by(self.Model.date).slice(start, stop))
        return q.scalars().all()
