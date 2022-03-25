from datetime import datetime

import pydantic

from sqlalchemy import Column, Integer, JSON
from sqlalchemy.future import select

from stattik.database import Repository, Model

from .schemata import PostConnection

class Post(pydantic.BaseModel):
    id: int
    title: str
    date: datetime
    description: str
    cover: str
    slug: str
    category: str

class Post(Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)

class PostRepository(Repository):
    model = Post
    async def create(self, data):
        post = Post(data=data)
        self.session.add(post)
        await self.session.flush()

    async def all(self):
        q = await self.session.execute(select(Post).order_by(Post.id))
        return q.scalars().all()

    @query("allPost")
    async def resolve_all(self, root, info, after='', before='', first=0, last=0):
        posts = await self.all()
        connection = PostConnection(posts)
        result = connection.wire()
        return result
