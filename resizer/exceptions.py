import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class BaseLambdaResponse(Exception):

    def __init__(self):
        self.headers = {}
        self.content_type = 'application/json'

    def get(self):
        self.headers.update({'Content-Type': self.content_type})
        response = {
            'statusCode': self.code,
            'headers': self.headers,
            'body': self.body
        }

        log_response = {
            'statusCode': self.code,
            'headers': self.headers,
            'body': '{0} ({1} bytes)'.format((self.body[:350] + ' [TRUNCATED]') if len(self.body) > 350 else self.body, len(self.body))
        }
        logger.info('Lambda response: {0}'.format(log_response))

        return response

class SuccessResponse(BaseLambdaResponse):

    def __init__(self, response):
        super(SuccessResponse, self).__init__()
        self.code = 200
        self.body = response.get('body', '')
        self.headers = response.get('headers', {})
        self.content_type = self.headers.get('Content-Type', 'application/json')

    def get(self):
        logger.info('HTTP {0}: Success'.format(self.code))
        return super(SuccessResponse, self).get()


class BaseLambdaErrorResponse(BaseLambdaResponse):

    def get(self):
        logger.error('HTTP {0}: {1}'.format(self.code, json.loads(self.body)['message']))
        return super(BaseLambdaErrorResponse, self).get()


class InternalErrorResponse(BaseLambdaErrorResponse):

    def __init__(self, message):
        super(InternalErrorResponse, self).__init__()
        self.code = 500
        self.body = json.dumps({'message': message})


class InvalidRequestResponse(InternalErrorResponse):

    def __init__(self, message):
        super(InvalidRequestResponse, self).__init__(message)
        self.code = 400


class FileNotFoundResponse(BaseLambdaErrorResponse):

    def __init__(self, bucket, key):
        super(FileNotFoundResponse, self).__init__()
        self.code = 404
        self.body = json.dumps({'message': 'Image "{0}" cannot be located in "{1}"'.format(key, bucket)})


class BucketNotFoundResponse(BaseLambdaErrorResponse):

    def __init__(self, bucket):
        super(BucketNotFoundResponse, self).__init__()
        self.code = 500
        self.body = json.dumps({'message': 'Origin bucket "{0}" doesn\'t exist or is inaccessible'.format(bucket)})
