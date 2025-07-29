import unittest
import os
from paystack4python.transactions import Transaction

class TestTransaction(unittest.TestCase):
    def setUp(self):
        os.environ['PAYSTACK_AUTHORIZATION_KEY'] = 'sk_test_xxx'
        self.tx = Transaction()

    def test_methods_exist(self):
        self.assertTrue(hasattr(self.tx, 'getall'))
        self.assertTrue(hasattr(self.tx, 'getone'))
        self.assertTrue(hasattr(self.tx, 'totals'))
        self.assertTrue(hasattr(self.tx, 'initialize'))
        self.assertTrue(hasattr(self.tx, 'charge'))
        self.assertTrue(hasattr(self.tx, 'verify'))
        self.assertTrue(hasattr(self.tx, 'fetch_transfer_banks'))
        self.assertTrue(hasattr(self.tx, 'create_transfer_customer'))
        self.assertTrue(hasattr(self.tx, 'transfer'))

if __name__ == '__main__':
    unittest.main()
