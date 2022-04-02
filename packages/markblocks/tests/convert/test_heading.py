import unittest
import itertools

from markblocks.data import load

from markblocks.convert import Converter

class Test(unittest.TestCase):
    def test(self):
        filename = "heading.md"
        with load(filename) as fh:
            text = fh.read()

        print("##start##")
        print(text)
        print("##end##")

        converter = Converter()
        result = converter.convert(text)
        print(result)

if __name__ == "__main__":
    unittest.main()
