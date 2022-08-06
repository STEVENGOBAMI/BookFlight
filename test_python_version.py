import sys
import unittest

class TestVersion(unittest.TestCase):
    def test_python_version(self):
        assert sys.version_info >= (
            3,
            9,
        )
        print(sys.version)


if __name__ == '__main__':
    unittest.main()

