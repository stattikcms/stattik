
from pathlib import Path

from stattik.scope import Scope

class Generator:
    def __init__(self, path, obj):
        self.path = path
        self.obj = obj
        self.name = obj.__name__
        self.scopes = []

    @property
    def scope(self):
        return self.scopes[-1]
    
    def begin(self, node=None):
        self.scopes.append(Scope(node))

    def end(self):
        return self.scopes.pop()

    def generate(self):
        path = self.path
        obj = self.obj
        #print(path)
        dst_path = Path(f"build/{'/'.join(path.parts[1:])}")
        #print(dst_path)
        self.begin()

        self.write_imports()
        self.write_model()
        
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dst_path, "w") as text_file:
            text_file.write(str(self.scope))

    def write_imports(self):
        self.scope(f"""
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.sqlite import JSON
from stattik.database import Model, Repository

from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
        """)
        self.scope.nl()

    def write_model(self):
        self.scope(f"""
class {self.name}(Model):
    id = Column(Integer, primary_key=True)
    data = Column(JSON)

class {self.name}Repo(Repository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, data):
        obj = {self.name}(**data)
        self.db_session.add(obj)
        await self.db_session.flush()

    async def all(self) -> List[{self.name}]:
        q = await self.db_session.execute(select({self.name}).order_by({self.name}.id))
        return q.scalars().all()
        """
        )