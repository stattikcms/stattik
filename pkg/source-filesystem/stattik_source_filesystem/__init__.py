from loguru import logger


class FileSystemSource:
    def __init__(self, app, options) -> None:
        self.app = app
        for key in options:
            setattr(self, key, options[key])

    @classmethod
    def produce(cls, app, options):
        plugin = cls(app, options)
        plugin.create()
        return plugin

    def create(self):
        pass


def install(app, options):
    logger.debug("install plugin")
    plugin = FileSystemSource.produce(app, options)
    return plugin
