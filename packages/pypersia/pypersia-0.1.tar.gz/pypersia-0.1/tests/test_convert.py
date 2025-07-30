import unittest
from pypersia.convert import convert_digits

class TestConvert(unittest.TestCase):
    def test_en_to_fa(self):
        self.assertEqual(convert_digits("123", "fa"), "۱۲۳")

if __name__ == "__main__":
    unittest.main()
