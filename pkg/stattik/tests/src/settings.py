import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite+aiosqlite:///./stattik.db'

'''
siteMetadata = {
    'title': 'Kurtis Fields',
    'description': 'Coder, Musician, and sometimes Artist',
}

apps = [
    'kfields_site.search'
]

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
'''