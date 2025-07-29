import unittest
from ukraine_phone_formatter import format_ukrainian_phone

class TestUkrainePhoneFormatter(unittest.TestCase):

    def test_format_10_digits(self):
        self.assertEqual(format_ukrainian_phone("0501234567"), "+38 (050) 123-45-67")

    def test_format_12_digits_with_38(self):
        self.assertEqual(format_ukrainian_phone("380679876543"), "+38 (067) 987-65-43")

    def test_format_with_plus(self):
        self.assertEqual(format_ukrainian_phone("+380995554433"), "+38 (099) 555-44-33")

    def test_format_with_parentheses_and_hyphens(self):
        self.assertEqual(format_ukrainian_phone("(093) 112-23-34"), "+38 (093) 112-23-34")

    def test_invalid_format(self):
        self.assertEqual(format_ukrainian_phone("invalid"), "invalid")
        self.assertEqual(format_ukrainian_phone("123"), "123")
        self.assertEqual(format_ukrainian_phone("050123456"), "050123456")

if __name__ == '__main__':
    unittest.main()