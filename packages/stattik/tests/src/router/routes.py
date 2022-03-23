routes = [
    {
        "path": "/",
        "component": "src/layouts/RootLayout",
        "children": [
            {"path": "", "component": "src/pages/Home"},
            {"path": "post", "component": "src/layouts/PostsLayout",
                "children": [
                    {"path": "", "component": "src/pages/Posts"},
                    {"path": "{postname}", "component": "src/pages/Post"},
                ]
            },
        ],
    }
]