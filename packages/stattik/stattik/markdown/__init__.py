import markdown

#md = markdown.Markdown(extensions=['extra', 'smarty', 'toc', 'tables', 'fenced_code'])
md = markdown.Markdown(
    extensions=[
        'toc',
        'pymdownx.highlight',
        #'pymdownx.extra',
        'pymdownx.emoji',
        'pymdownx.superfences',
    ],
    extension_configs={
        'pymdownx.highlight': {
            'auto_title': True
        }
    }
)

'''
extension_configs=[

]
'''
