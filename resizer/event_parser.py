import re
import logging

from exceptions import InvalidRequestResponse


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse_from(event):
    '''
    Extract and parse relevant information from the Lambda's event object
    '''
    data = parse_uri(event['path'])
    data.update(parse_headers(event['headers']))
    logger.info('Resizer Lambda called with the following data: {0}'.format(data))

    return data


def parse_headers(headers):
    headers = headers or {}
    return {
        'meta': {
            'Amazon-Request-Id': headers.get('X-Amzn-Trace-Id'),
            'Supported-Image-Formats': re.findall('image/(\w+)', headers.get('Accept', ''))
        }
    }


def parse_uri(path):
    '''
    Parse URI into it's components
    '''
    try:
        dimensions, ops, sha, image_format = re.findall('(\d+x\d+)-?([^/]*)/([a-fA-F0-9]{64})/.*\.(gif|jpe?g|png)$', path)[0]
        operations = map(lambda op: op.split('='), ops.split(',')) if ops != '' else []
        w, h = [int(x) for x in dimensions.split('x')]
    except:
        raise InvalidRequestResponse('Invalid request URI. Got "{0}"'.format(path))

    return {
        'operations': operations,
        'requested_image': {
            'width': w,
            'height': h
        },
        'original_image': {
            'format': image_format,
            'url': '{0}.{1}'.format(sha, image_format)
        }
    }
