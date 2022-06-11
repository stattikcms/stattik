import unittest

from markblocks.data import load
from markblocks import Markblocks

class Test(unittest.TestCase):
    def test(self):
        filename = "ul.md"
        with load(filename) as fh:
            text = fh.read()

        print("##start##")
        print(text)
        print("##end##")

        mb = Markblocks()
        result = mb.convert(text)
        print(result)

if __name__ == "__main__":
    unittest.main()
