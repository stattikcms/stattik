import unittest

import sys
sys.path.append("./src")

from datetime import datetime

from sqlalchemy import Column, Integer, JSON
from sqlalchemy.future import select

from stattik.database import Database, Repository
from stattik.model import Model
from stattik.data import Data

class Post(Model):
    id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)

class PostData(Data):
    id: int
    title: str
    date: datetime
    description: str
    cover: str
    slug: str

class PostInput(Data):
    title: str
    date: datetime
    description: str
    cover: str
    slug: str

class PostRepository(Repository):
    Model = Post
    async def create(self, session, data):
        post = Post(data=data)
        session.add(post)
        await session.flush()

    async def all(self, session):
        q = await session.execute(select(Post).order_by(Post.id))
        return q.scalars().all()

date_format = "%Y-%m-%d %H:%M:%S"
items = [
    {
        "title": "Hello World",
        "date": datetime.strptime("2018-09-14 07:42:34", date_format),
        "description": "A developer blog is born",
        "cover": "https://i.imgur.com/Uv6nv7k.jpg",
        "slug": "hello-world",
    },
    {
        "title": "New Blog Design",
        "date": datetime.strptime("2019-07-08 10:46:34", date_format),
        "description": "New Blog Design",
        "cover": "https://i.imgur.com/S8eaSMh.jpg",
        "slug": "new-blog-design",
    }
]
class Test(unittest.IsolatedAsyncioTestCase):
    async def test(self):
        db = Database.produce()
        repo = PostRepository.produce(db)
        print(repo.__dict__)

        await db.drop_all()
        await db.begin()
        async with db.Session() as session:
            async with session.begin():
                for item in items:
                    pod = PostInput(**item)
                    await repo.create(session, pod)

                all = await repo.all(session)
                print(all)

        # Gives us a chance to inspect the database when ran manually:  python test_repository.py
        if not "pytest" in sys.modules:
            input("Press Enter to Exit...")

        #await db.drop_all()

if __name__ == "__main__":
    unittest.main()
