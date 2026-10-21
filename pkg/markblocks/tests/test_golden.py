import os
import unittest

from markblocks.data import load
from markblocks import Markblocks

golden_dir = os.path.join(os.path.dirname(__file__), 'golden')

# Inputs that the grammar rejects; convert() returns None for these.
invalid = ['html.md', 'tag.md']

class Test(unittest.TestCase):
    def test_golden(self):
        for filename in sorted(os.listdir(golden_dir)):
            name = filename[:-len('.html')]
            with self.subTest(name=name):
                with load(f"{name}.md") as fh:
                    text = fh.read()
                with open(os.path.join(golden_dir, filename)) as fh:
                    expected = fh.read()
                self.assertEqual(Markblocks().convert(text), expected)

    def test_invalid(self):
        for filename in invalid:
            with self.subTest(name=filename):
                with load(filename) as fh:
                    text = fh.read()
                self.assertIsNone(Markblocks().convert(text))

if __name__ == "__main__":
    unittest.main()
