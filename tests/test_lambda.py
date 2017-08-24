import unittest
import importlib

Lambda = importlib.import_module('lambda')


class TestLambda(unittest.TestCase):

    def test_response_is_a_dict(self):
        return_value = Lambda.entrypoint({'path': ''}, None)
        self.assertIsInstance(return_value, dict)

    def test__response_is_in_expected_format(self):
        return_value = Lambda.entrypoint({'path': ''}, None)
        expected_keys = ['body', 'headers', 'statusCode']
        self.assertEqual(return_value.keys(), expected_keys)
