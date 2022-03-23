import unittest

import sys
sys.path.append("./src")

from stattik.schema import Schema, RootSchema

class HelloSchema(Schema):
    """
    extend type Query {
        counter: Int!
    }
    """
    @query("counter")
    async def counter_query(self, root, info):
        return 'Hi!'

class Test(unittest.IsolatedAsyncioTestCase):
    async def test(self):
        root = RootSchema.produce()
        schema = HelloSchema.produce(root)
        xschema = root.make_executable()

        gql = root.get_gql()
        print(gql)

        print(xschema)
        print(xschema.__dict__)

if __name__ == "__main__":
    unittest.main()
