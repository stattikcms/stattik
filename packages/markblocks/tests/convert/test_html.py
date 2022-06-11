import unittest
import itertools

from markblocks.data import load
from markblocks import Markblocks

class Test(unittest.TestCase):
    def test(self):
        filename = "html.md"
        with load(filename) as fh:
            text = fh.read()

        mb = Markblocks()
        result = mb.convert(text)
        print(result)

if __name__ == "__main__":
    unittest.main()
