import os

from .models import create_database
from .router import create_router
from .architect import create_architect
from .renderer import create_renderer
from .indexer import create_indexer
from .baker import create_baker

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite+aiosqlite:///./stattik.db'

def on_create(self):
    self.database = create_database()
    self.router = create_router()
    self.architect = create_architect()
    self.renderer = create_renderer()
    self.indexer = create_indexer()
    self.baker = create_baker()


siteMetadata = {
    'title': 'Kurtis Fields',
    'description': 'Coder, Musician, and sometimes Artist',
}

apps = [
    'stattik_theme_bulma',
    'stattik_app_search_fuse_bulma'
]

plugins = [
    {
        'use': 'stattik_plugin_search_fuse',
        'options': {
        }
    },
]

collections = [
    {
        'name': 'Post',
        'source': [
            {
                'use': 'stattik_source_filesystem',
                'options': {
                    'path': 'blog/*.md',
                    'route': '/blog/:slug'
                }
            },
        ]
    }
]