import unittest
import mock

import resizer


class TestResizer(unittest.TestCase):

    @mock.patch('os.environ.get', return_value='foo')
    def test_bucket_from_env(self, mocked_environ):
        self.assertEqual(resizer.bucket(), 'foo')
        mocked_environ.assert_called_once_with('SOURCE_IMAGES_BUCKET')

    @mock.patch('resizer.get_total_run_time_for', return_value=1)
    def test_run_times(self, mocked_get_total_run_time_for):
        expected_response = {'s3': 1, 'vips': 2}
        self.assertEqual(resizer.run_times(), expected_response)

    def test_response_dict(self):
        expected_response = {'code': 200, 'body': 'foo', 'headers': 'bar'}
        self.assertEqual(resizer.response_dict('foo', 'bar'), expected_response)

    def test_run_(self):
        # TODO
        pass
