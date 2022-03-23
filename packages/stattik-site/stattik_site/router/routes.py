routes = [
    {
        "path": "/",
        "component": "src/layouts/RootLayout",
        "children": [
            {"path": "", "component": "src/pages/Home"},
            {"path": "news", "component": "src/layouts/PostsLayout",
                "children": [
                    {"path": "", "component": "src/pages/Posts"},
                    {"path": "{postname}", "component": "src/pages/Post"},
                ]
            },
            {"path": "docs", "component": "src/layouts/DocsLayout",
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