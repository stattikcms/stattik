from pathlib import Path
from types import SimpleNamespace

import pytest

from stattik.architect.builders import FolderBuilder, Job, MarkdownBuilder
from stattik.database import create_database
from stattik.markdown import Markdown
from stattik.menu import build_bottom_up, build_matched
from stattik.repositories.page import PageRepository

PAGES = {
    "content/_index.md": "---\ntitle: Home\n---\nHome",
    "content/docs/_index.md": "---\ntitle: Docs\nmenu:\n    - title: A\n      url: a\n---\nDocs",
    "content/docs/a.md": "---\ntitle: A\n---\nA",
}


@pytest.fixture
async def db(tmp_path, monkeypatch):
    for name, text in PAGES.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    # NOTE: Builders work with paths relative to the site root, like content/docs/a.md
    monkeypatch.chdir(tmp_path)
    # NOTE: The real Markdown needs a whole Site, and the body doesn't matter here
    monkeypatch.setattr(Markdown, "_instance", SimpleNamespace(md=SimpleNamespace(convert=lambda text: text)))

    db = create_database([PageRepository])
    await db.begin("memory://")
    builder = FolderBuilder()
    builder.builders = {".md": MarkdownBuilder}
    await builder.build(Job(Path("content"), {"type": "Page", "db": db, "parent": None}))
    await db.end_session()
    yield db
    await db.close()


async def page(db, url):
    return await db["Page"].find_by_url(url)


async def test_parents(db):
    home, docs, a = [await page(db, url) for url in ("/", "/docs", "/docs/a.html")]
    assert a.parent is docs
    assert docs.parent is home
    assert home.parent is None
    assert list(docs.children) == [a]


async def test_menu_urls_are_strings(db):
    docs = await page(db, "/docs")
    assert docs.menu == [{"title": "A", "url": "/docs/a.html"}]


async def test_side_menu(db):
    docs, a = await page(db, "/docs"), await page(db, "/docs/a.html")
    assert build_matched(a) == [docs, a]
    menu = build_bottom_up(a)
    assert menu.title == "Docs"
    [item] = menu.children
    assert (item.title, item.cls, item.url) == ("A", "is-active", "#")
