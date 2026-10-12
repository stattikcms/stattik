class Collection:
    def __init__(self):
        self.type = self.__class__.__name__

    def inject(self, data):
        for key in data:
            setattr(self, key, data[key])

    @classmethod
    def produce(self, data):
        collection = factories[data['type']](data)
        return collection
'''
class Pagination(Collection):
    def __init__(self, data):
        super().__init__(data)


factories = {
    'Pagination': Pagination
}
'''