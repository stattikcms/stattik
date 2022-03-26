routes = [
    {
        "path": "/",
        "component": "src/layouts/RootLayout",
        "children": [

            {"path": "", "component": "src/pages/Home"},

            {"path": "search", "component": "src/layouts/SearchLayout",
                "children": [
                    {"path": "", "component": "src/pages/Search"},
                ]
            },

            {"path": "blog", "component": "src/layouts/PostsLayout",
                "children": [
                    {"path": "", "component": "src/pages/Posts"},
                    {"path": "page/{number:int}/", "component": "src/pages/Posts"},
                    {"path": "{postname}", "component": "src/pages/Post"},
                ]
            },
        ],
    }
]