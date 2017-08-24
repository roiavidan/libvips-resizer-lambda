import logging
import os
import json
import time

from vips import image_from_buffer, process_image, image_get_dimensions
from repositories.s3 import get_image
from exceptions import SuccessResponse
from timing import get_total_run_time_for
from svg import embed


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run(data):
    logger.info('Requested image size is {0}x{1}'.format(data['requested_image']['width'], data['requested_image']['height']))

    # Get original image from S3
    image_buffer = get_image(bucket(), data['original_image']['url'])
    image = image_from_buffer(image_buffer)

    # Get image dimensions
    original_image_width, original_image_height = image_get_dimensions(image)
    data['original_image'].update({'width': original_image_width, 'height': original_image_height})
    logger.info('Original image size is {0}x{1}'.format(original_image_width, original_image_height))

    # Get the new image after applying transformations to it
    image_buffer = process_image(image_buffer, data)
    logger.info('New image size is {0}x{1}'.format(data['resized_image']['width'], data['resized_image']['height']))

    # Prepare response headers with useful information
    headers = {
        'Content-Type': 'image/svg+xml',
        'X-Resized-Width': data['resized_image']['width'],
        'X-Resized-Height': data['resized_image']['height'],
        'X-Original-Width': original_image_width,
        'X-Original-Height': original_image_height,
        'X-Original-Format': data['original_image']['format'],
        'X-Server-Timing': 'miss, s3={s3:.3f}, vips={vips:.3f}'.format(**run_times())
    }

    # Response is always raised, not returned
    raise SuccessResponse(response_dict(
        embed(image_buffer, data),
        headers
    ))


def bucket():
    return os.environ.get('SOURCE_IMAGES_BUCKET')


def run_times():
    return {
        's3': get_total_run_time_for('s3'),
        'vips': get_total_run_time_for('image_transformations') + get_total_run_time_for('image_from_buffer')
    }


def response_dict(body, headers):
    return {
        'code': 200,
        'headers': headers,
        'body': body
    }
