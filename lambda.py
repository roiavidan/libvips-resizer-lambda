#!/usr/bin/python

import resizer
import logging
import json

BUCKET = 'mybuket'
KEY = 'test.jpg'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def extract_request_info_from_event(event):
    if event['httpMethod'] != 'GET':
        raise Exception('Unsupported HTTP method {0}'.format(event['httpMethod']))

    return {
        'path': event['path'],
        'headers': event['headers'],
        'qs': event['queryStringParameters']
    }


def entrypoint(event, context):
    logger.info('event {0}'.format(event))
    logger.info('context {0}'.format(context))
    # orig_image = pylibs.s3.download(BUCKET, KEY)
    # print pylibs.vips.thumbnail(orig_image.name)
    request = extract_request_info_from_event(event)

    logger.info('info logger from lambda')
    #print resizer.vips.thumbnail('test.jpg')
    return respond(None, 'hello from resizer lambda. request: {0}'.format(json.dumps(request)))


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'text/html',
            'X-Roi': 'lambda'
        },
    }



# Only run from command line (simulate Lambda execution)
if __name__ == '__main__':
    entrypoint(None, None)
