import os

from .routes import routes

SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
DATABASE_URL = os.environ.get("DATABASE_URL") or "sqlite:///./stattik.db"

page_types = ["Landing", "Post", "Project"]


siteMetadata = {
    "title": "Stattik",
    "description": "Static Site Generator in Python",
}

apps = [
    "stattik_theme_bulma",
]

plugins = []
"""
plugins = [
    {
        'use': 'stattik_source_filesystem',
        'options': {
            'path': 'blog/*.md',
            'typeName': 'Post',
            'route': '/blog/:slug'
        }
    },
]
"""

collections = [
    {
        "name": "Post",
        "source": [
            {
                "use": "stattik_source_filesystem",
                "options": {"path": "blog/*.md", "route": "/blog/:slug"},
            },
        ],
    }
]
