from stattik.schema import Schema

class Repository(Schema):
    def __init__(self, parent):
        super().__init__(parent)
