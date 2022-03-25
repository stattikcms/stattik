import os

root = 'kfields_site'

environment = {
    "STATTIK_ROOT_MODULE": 'kfields_site',
    'STATTIK_SETTINGS_MODULE': 'kfields_site.settings'
}

resolve = {
    'alias': {
        "@": os.path.abspath(os.path.join(os.path.dirname(__file__), root)),
        "src": os.path.abspath(os.path.join(os.path.dirname(__file__), root))
    },
}
