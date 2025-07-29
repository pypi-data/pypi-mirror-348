import unittest
from paystack4python.utils import validate_amount, validate_interval
from paystack4python.errors import InvalidDataError

class TestUtils(unittest.TestCase):
    def test_validate_amount_valid(self):
        self.assertEqual(validate_amount(1000), 1000)
        self.assertEqual(validate_amount(0), 0)
        self.assertEqual(validate_amount(10.5), 10.5)

    def test_validate_amount_invalid(self):
        with self.assertRaises(InvalidDataError):
            validate_amount(None)
        with self.assertRaises(InvalidDataError):
            validate_amount("abc")
        with self.assertRaises(InvalidDataError):
            validate_amount(-10)

    def test_validate_interval_valid(self):
        for interval in ['hourly', 'daily', 'weekly', 'monthly', 'annually']:
            self.assertEqual(validate_interval(interval), interval)

    def test_validate_interval_invalid(self):
        with self.assertRaises(InvalidDataError):
            validate_interval('biweekly')

if __name__ == '__main__':
    unittest.main()
