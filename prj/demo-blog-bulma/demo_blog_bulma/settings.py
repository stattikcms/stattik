import os

from .routes import routes

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///./stattik.db'


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