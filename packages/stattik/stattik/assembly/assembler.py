import os
import shutil
import asyncio
import inspect
import importlib.util
from pathlib import Path

from loguru import logger
from pydantic import BaseModel

from stattik.site import Site
from .generator import Generator

from ariadne import load_schema_from_path
from graphql import (
    parse,
    ObjectTypeDefinitionNode,
)

class Assembler:
    def __init__(self):
        pass

    async def assemble(self):
        site = Site.instance
        schema_string = load_schema_from_path("./src/models")
        print(schema_string)
        document = parse(schema_string)
        print(document.definitions)
        for node in document.definitions:
            if isinstance(node, ObjectTypeDefinitionNode):
                self.parse_object_type(node)

    """
    interfaces: FrozenList[NamedTypeNode]
    directives: FrozenList[ConstDirectiveNode]
    fields: FrozenList["FieldDefinitionNode"]
    """
    def parse_object_type(self, node):
        for field in node.fields:
            self.parse_field(field)

    """
    description: Optional[StringValueNode]
    name: NameNode
    directives: FrozenList[ConstDirectiveNode]
    arguments: FrozenList["InputValueDefinitionNode"]
    type: TypeNode
    """
    def parse_field(self, field):
        #print(field.type)
        pass

    def load_module(self, path):
        spec = importlib.util.spec_from_file_location(
            str(path), path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module