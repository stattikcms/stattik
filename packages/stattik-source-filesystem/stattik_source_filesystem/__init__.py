from loguru import logger 

class FileSystemSource:
    def __init__(self, app, options) -> None:
        self.app = app
        for key in options:
            setattr(self, key, options[key])

    @classmethod
    def produce(self, app, options):
        plugin = self(app, options)
        plugin.create()
        return plugin

    def create(self):
        pass
'''
@query.field("allPost")
def resolve_all_post(*_):
    #posts = Post.select()
    posts = [p for p in Post.select()]
    connection = PostConnection(posts)
    result = connection.wire()
    #print(result)
    return result
'''
    
def install(app, options):
    logger.debug('install plugin')
    plugin = FileSystemSource.produce(app, options)
    return plugin