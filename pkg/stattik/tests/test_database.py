import unittest
from datetime import datetime
from pathlib import Path

from stattik.database import create_database
from stattik.repositories.page import PageRepository, define_page_type

URL = "memory://"


class Test(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        Post = define_page_type("Post")
        self.db = create_database([PageRepository, Post])
        await self.db.begin(URL)
        await self.db.reset()
        self.posts = self.db["Post"]
        for day, slug in [(1, "first"), (3, "third"), (2, "second")]:
            await self.posts.create({
                "type": "Post",
                "title": slug,
                "date": datetime(2024, 1, day),
                "src_url": Path(f"/_index/{slug}"),
                "url": Path(f"/{slug}"),
            })
        await self.posts.create({"type": "Post", "title": "undated"})
        await self.db.end_session()

    async def asyncTearDown(self):
        await self.db.close()
        self.assertIsNone(self.db.kv)

    async def test_begin_is_idempotent(self):
        kv = self.db.kv
        await self.db.begin(URL)
        self.assertIs(self.db.kv, kv)

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

    async def test_find_by_src_url_is_a_post(self):
        page = await self.db["Page"].find_by_src_url("/_index/third")
        self.assertEqual(type(page).__name__, "Post")
        self.assertEqual(page.src_url, Path("/_index/third"))

    async def test_extras_and_parent(self):
        parent = await self.db["Page"].find_by_url("/first")
        child = await self.posts.create({
            "type": "Post",
            "title": "child",
            "parent": parent,
            "db": self.db,
            "tags": ["a", "b"],
        })
        await self.db.end_session()
        self.assertIs(child.parent, parent)
        self.assertEqual(child.tags, ["a", "b"])
        self.assertNotIn("db", child.extras)

    async def test_sqlite(self):
        db = create_database([PageRepository])
        await db.begin("sqlite:///:memory:")
        await db["Page"].create({"type": "Page", "title": "x", "url": Path("/x")})
        await db.end_session()
        self.assertEqual((await db["Page"].find_by_url("/x")).title, "x")
        await db.reset()
        self.assertEqual(await db["Page"].count(), 0)
        await db.close()

    async def test_reset(self):
        await self.db.reset()
        self.assertEqual(await self.posts.count(), 0)


if __name__ == "__main__":
    unittest.main()
