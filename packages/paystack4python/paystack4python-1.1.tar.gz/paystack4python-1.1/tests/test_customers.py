import unittest
import os
from paystack4python.customers import Customer

class TestCustomer(unittest.TestCase):
    def setUp(self):
        os.environ['PAYSTACK_AUTHORIZATION_KEY'] = 'sk_test_xxx'
        self.customer = Customer()

    def test_methods_exist(self):
        self.assertTrue(hasattr(self.customer, 'create'))
        self.assertTrue(hasattr(self.customer, 'update'))
        self.assertTrue(hasattr(self.customer, 'getall'))
        self.assertTrue(hasattr(self.customer, 'getone'))

if __name__ == '__main__':
    unittest.main()
