from sqlalchemy.orm import DeclarativeBase, declared_attr

class ModelMixin:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__

class Model(ModelMixin, DeclarativeBase):
    __abstract__ = True

