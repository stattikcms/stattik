from stattik.schema import Schema

class Repository(Schema):
    def __init__(self, parent):
        super().__init__(parent)
    
    @classmethod
    def produce(cls, parent):
        return cls(parent)