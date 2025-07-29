import unittest
import os
from paystack4python.plans import Plan

class TestPlan(unittest.TestCase):
    def setUp(self):
        os.environ['PAYSTACK_AUTHORIZATION_KEY'] = 'sk_test_xxx'
        self.plan = Plan()

    def test_methods_exist(self):
        self.assertTrue(hasattr(self.plan, 'create'))
        self.assertTrue(hasattr(self.plan, 'update'))
        self.assertTrue(hasattr(self.plan, 'getall'))
        self.assertTrue(hasattr(self.plan, 'getone'))

if __name__ == '__main__':
    unittest.main()
