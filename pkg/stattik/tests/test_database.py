import unittest
from datetime import datetime
from pathlib import Path

from stattik.database import create_database
from stattik.repositories.page import PageRepository, define_page_type

URL = "sqlite+aiosqlite:///:memory:"


class Test(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        Post = define_page_type("Post")
        self.db = create_database([PageRepository, Post])
        await self.db.begin(URL)
        await self.db.reset()
        self.posts = self.db["Post"]
        for day, slug in [(1, "first"), (3, "third"), (2, "second")]:
            await self.posts.add(self.posts.Model({
                "type": "Post",
                "title": slug,
                "date": datetime(2024, 1, day),
                "src_url": Path(f"/_index/{slug}"),
                "url": Path(f"/{slug}"),
            }))
        await self.posts.add(self.posts.Model({"type": "Post", "title": "undated"}))
        await self.db.end_session()

    async def asyncTearDown(self):
        await self.db.close()
        self.assertIsNone(self.db.engine)

    async def test_begin_is_idempotent(self):
        engine = self.db.engine
        await self.db.begin(URL)
        self.assertIs(self.db.engine, engine)

    async def test_count(self):
        self.assertEqual(await self.posts.count(), 4)
        self.assertEqual(await self.db["Page"].count(), 4)

    async def test_latest_is_newest_first(self):
        posts = await self.posts.latest(0, 3)
        # The undated post defaults to now, so it is the newest
        self.assertEqual([p.title for p in posts], ["undated", "third", "second"])

    async def test_find_by_src_url(self):
        page = await self.posts.find_by_src_url("/_index/second")
        self.assertEqual(page.title, "second")
        self.assertIsNone(await self.posts.find_by_src_url("/second"))

    async def test_find_by_url(self):
        page = await self.posts.find_by_url("/second")
        self.assertEqual(page.title, "second")
        self.assertIsNone(await self.posts.find_by_url("/_index/second"))

    async def test_reset(self):
        await self.db.reset()
        self.assertEqual(await self.posts.count(), 0)


if __name__ == "__main__":
    unittest.main()
