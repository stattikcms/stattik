routes = [
    {
        "path": "/",
        "component": "src/layouts/RootLayout",
        "children": [
            {"path": "_index", "component": "src/layouts/DocsLayout",
                "children": [
                    {"path": "", "component": "src/pages/Docs"},
                    {"path": "start",
                        "children": [
                            {"path": "", "component": "src/pages/Doc"},
                            {"path": "{docname}", "component": "src/pages/Doc"},
                        ]
                    },
                    {"path": "{docname}", "component": "src/pages/Doc"},
                ]
            },
        ],
    }
]