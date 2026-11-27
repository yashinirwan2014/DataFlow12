import unittest
from main import clean_text

class Tests(unittest.TestCase):
    def test_trim(self):
        self.assertEqual(clean_text("  data  "), "data")
    def test_empty(self):
        self.assertEqual(clean_text(None), "")

if __name__ == "__main__":
    unittest.main()
