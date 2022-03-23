import unittest
import itertools

import sys
sys.path.append("./src")

from stattik.site import Site


class Test(unittest.TestCase):
    def test(self):
        site = Site.instance

if __name__ == "__main__":
    unittest.main()
