import unittest
import os
from paystack4python.errors import MissingAuthKeyError, InvalidMethodError

class TestBaseAPI(unittest.TestCase):
    def test_missing_auth_key(self):
        if 'PAYSTACK_AUTHORIZATION_KEY' in os.environ:
            del os.environ['PAYSTACK_AUTHORIZATION_KEY']
        from paystack4python.baseapi import BaseAPI
        with self.assertRaises(MissingAuthKeyError):
            BaseAPI()

    def test_invalid_method(self):
        os.environ['PAYSTACK_AUTHORIZATION_KEY'] = 'sk_test_xxx'
        from paystack4python.baseapi import BaseAPI
        api = BaseAPI()
        with self.assertRaises(InvalidMethodError):
            api._handle_request('PATCH', 'https://api.paystack.co/test')

if __name__ == '__main__':
    unittest.main()
