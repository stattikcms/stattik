import os

from .routes import routes

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite+aiosqlite:///./stattik.db'

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
