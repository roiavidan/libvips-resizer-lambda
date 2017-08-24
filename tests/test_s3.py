import unittest
import mock

import io
import botocore

from resizer.exceptions import BucketNotFoundResponse, FileNotFoundResponse, InternalErrorResponse
from resizer.repositories.s3 import get_image

EXPECTED_IMAGE_BASE64_DATA = 'foobarmehneh'


def _object_with_no_bucket(self, operation_name, kwargs):
    resp = {'Error': {'Code': 'NoSuchBucket', 'BucketName': kwargs.get('Bucket')}}
    raise botocore.exceptions.ClientError(resp, 'foo')

def _get_object_with_no_image(self, operation_name, kwargs):
    resp = {'Error': {'Code': 'NoSuchKey', 'Key': kwargs.get('Key')}}
    raise botocore.exceptions.ClientError(resp, 'foo')

def _get_object_with_no_image_access_denied(self, operation_name, kwargs):
    resp = {'Error': {'Code': 'AccessDenied'}}
    raise botocore.exceptions.ClientError(resp, 'foo')

def _get_object_success(self, operation_name, kwargs):
    resp = {'Body': io.BytesIO(EXPECTED_IMAGE_BASE64_DATA.encode('utf-8'))}
    return resp


class TestS3Repository(unittest.TestCase):

    @mock.patch('botocore.client.BaseClient._make_api_call', new=_object_with_no_bucket)
    def test_missing_bucket_on_get_image(self):
        with self.assertRaises(BucketNotFoundResponse):
            get_image('foo_bucket', 'bar_file')

    @mock.patch('botocore.client.BaseClient._make_api_call', new=_get_object_with_no_image)
    def test_missing_file_on_get_image(self):
        with self.assertRaises(FileNotFoundResponse):
            get_image('foo_bucket', 'bar_file')

    @mock.patch('botocore.client.BaseClient._make_api_call', new=_get_object_with_no_image_access_denied)
    def test_access_denied_on_get_image(self):
        with self.assertRaises(InternalErrorResponse):
            get_image('foo_bucket', 'bar_file')

    @mock.patch('botocore.client.BaseClient._make_api_call', new=_get_object_success)
    def test_get_image(self):
        self.assertEqual(get_image('foo_bucket', 'bar_file'), EXPECTED_IMAGE_BASE64_DATA)
