import os

root = 'demo_miniblog_bulma'

environment = {
    "STATTIK_ROOT_MODULE": root,
    'STATTIK_SETTINGS_MODULE': f"{root}.settings"
}

resolve = {
    'alias': {
        "@": os.path.abspath(os.path.join(os.path.dirname(__file__), root)),
        "src": os.path.abspath(os.path.join(os.path.dirname(__file__), root))
    },
}
