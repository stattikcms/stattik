class Job:
    def __init__(self, src_path, config={}) -> None:
        self.src_path = src_path
        self.config = config
        self.inject(config)

    def inject(self, data, prefix=''):
        for key in data:
            setattr(self, f"{prefix}{key}", data[key])
