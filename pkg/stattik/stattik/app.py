from .vue import Vue

class App(Vue):
    instance = None

    def __init__(self, props={}):
        super().__init__(props)
        App.instance = self
    
    @classmethod
    async def produce(self, props):
        #print(props)
        if self.instance:
            self.instance.inject(props)
            return self.instance
        self.instance = await super().produce(props)
        return self.instance

    def component(self, name, klass):
        super().component(name, klass)
        self.global_components[name] = klass
