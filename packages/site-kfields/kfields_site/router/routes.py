routes = [
    {
        "path": "/",
        "component": "src/layouts/RootLayout",
        "children": [

            {"path": "", "component": "src/pages/Home"},

            {"path": "about", "component": "src/layouts/AboutLayout",
                "children": [
                    {"path": "", "component": "src/pages/About"},
                ]
            },

            {"path": "contact", "component": "src/layouts/ContactLayout",
                "children": [
                    {"path": "", "component": "src/pages/Contact"},
                ]
            },

            {"path": "search", "component": "src/layouts/SearchLayout",
                "children": [
                    {"path": "", "component": "src/pages/Search"},
                ]
            },

            {"path": "post", "component": "src/layouts/PostsLayout",
                "children": [
                    {"path": "", "component": "src/pages/Posts"},
                    {"path": "page/{number:int}/", "component": "src/pages/Posts"},
                    {"path": "{postname}", "component": "src/pages/Post"},
                ]
            },
            {"path": "project", "component": "src/layouts/ProjectsLayout",
                "children": [
                    {"path": "", "component": "src/pages/Projects"},
                    {"path": "page/{number:int}/", "component": "src/pages/Projects"},
                    {"path": "{postname}", "component": "src/pages/Project"},
                ]
            },
        ],
    }
]