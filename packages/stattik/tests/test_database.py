import unittest

import sys
sys.path.append("./src")

from stattik.database import Database

class Test(unittest.IsolatedAsyncioTestCase):
    async def test(self):
        database = Database.produce()

if __name__ == "__main__":
    unittest.main()
