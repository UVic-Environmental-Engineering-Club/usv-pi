import unittest


class TestDriver(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(1+2+3, 6, "Should be 6")

    def test_bad(self):
        self.assertEqual(False, False)

if __name__ == '__main__':
    unittest.main()