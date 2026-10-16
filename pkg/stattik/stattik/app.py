from .vue import Vue

class App(Vue):
    instance = None

    def __init__(self, props={}):
        super().__init__(props)
        App.instance = self
    
    @classmethod
    async def produce(cls, props):
        #print(props)
        if cls.instance:
            cls.instance.inject(props)
            return cls.instance
        cls.instance = await super().produce(props)
        return cls.instance

    def component(self, name, klass):
        super().component(name, klass)
        self.global_components[name] = klass
