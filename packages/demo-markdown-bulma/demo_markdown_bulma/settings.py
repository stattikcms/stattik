import os

from .models import create_database
from .router import create_router
from .architect import create_architect
from .renderer import create_renderer
from .indexer import create_indexer

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite+aiosqlite:///./stattik.db'

def on_create(self):
    self.database = create_database()
    self.router = create_router()
    self.architect = create_architect()
    self.renderer = create_renderer()
    self.indexer = create_indexer()

resolve = {
    'alias': {
        "@": os.path.abspath(os.path.dirname(__file__)),
        "src": os.path.abspath(os.path.dirname(__file__))
    },
}

site_metadata = {
    'title': 'Stattik',
    'description': 'Static Site Generator in Python',
}

apps = [
    'stattik_theme_bulma',
]

plugins = []
