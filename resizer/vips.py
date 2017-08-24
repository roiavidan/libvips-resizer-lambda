import pyvips
import logging

from timing import record_run_time_for


logger = logging.getLogger()
logger.setLevel(logging.INFO)


DEFAULT_QUALITY = 75
DEFAULT_OP = 'crop'
DEFAULT_FORMAT = 'jpg'
MUTUALLY_EXCLUSIVE_OPERATIONS = ['resize', 'crop', 'smart', 'fit']


def image_get_dimensions(image):
    '''
    Return the width and height of the given image
    '''
    return [image.width, image.height]


@record_run_time_for(name='image_from_buffer')
def image_from_buffer(image_data):
    '''
    Transform an image buffer (string) into a Vips Image object
    '''
    return pyvips.Image.new_from_buffer(image_data, '')


@record_run_time_for('image_transformations')
def process_image(image_buffer, data):
    '''
    Apply the requested transformations (operations) on the input image and return an output
    image object
    '''
    already_performed_mutually_exclusive_op = False
    new_image_buffer = None
    padding = False
    quality = DEFAULT_QUALITY
    fmt = DEFAULT_FORMAT
    func = None
    for op in (data['operations'] or [[DEFAULT_OP]]):
        op_name = op[0]
        if (func is None) and (op_name in MUTUALLY_EXCLUSIVE_OPERATIONS):
            func = globals()['operation_{0}'.format(op_name)]
        elif op_name == 'format':
            fmt = op[1]
        elif op_name == 'quality':
            quality = int(op[1])

    logger.info('Going to perform "{0}" to "{1}" with quality "{2}"'.format(func.__name__, fmt, quality))
    new_image, use_padding = func(new_image_buffer or image_buffer, data, op)
    if use_padding:
        padding = True

    data.update({
        'padding': padding,
        'resized_image': {'width': new_image.width, 'height': new_image.height}
    })

    return new_image.write_to_buffer('.{0}'.format(fmt), Q=quality)


def operation_resize(image_buffer, data, _op):
    '''
    Returns an image where the original image is wrapped by a rectangle with the requested
    proportions (white border is appended to the original image).
    '''
    return pyvips.Image.thumbnail_buffer(
        image_buffer,
        data['requested_image']['width'],
        height=data['original_image']['height']), True


def operation_crop(image_buffer, data, _op):
    '''
    Returns a portion of the original image cropped by a rectangle with the requested proportions.
    This is the default operation, if none is specified.
    '''
    return pyvips.Image.thumbnail_buffer(
        image_buffer,
        data['requested_image']['width'],
        height=data['requested_image']['height'], crop=True), False


def operation_smart(image_buffer, data, _op):
    '''
    Performs crop or resize operation. The decision logic is as follows:
        1. Let N = percentage of the original image covered by the cropped image.
        2. Return crop if N >= threshold
        3. Return resize otherwise
    The threshold is by default set to 60%, but can be overridden: /500x500-smart=75/{sha}/main.jpg
    '''
    threshold = (int(_op[1]) if len(_op) > 1 else 60) / 100.0
    if area_covered_by_crop(data) >= threshold:
        return operation_crop(image_buffer, data, _op)
    else:
        return operation_resize(image_buffer, data, _op)


def operation_fit(image_buffer, data, _op):
    '''
    Returns a resized version of original image with unchanged aspect ratio.
    The output image will fit into a rectangle defined by the requested dimensions,
    but will NOT have the same proportions as the requested dimensions.
    '''
    new_image_buffer, _ = operation_resize(image_buffer, data, _op)
    return new_image_buffer, False


def area_covered_by_crop(data):
    req_ar = float(data['requested_image']['width']) / float(data['requested_image']['height'])
    orig_ar = float(data['original_image']['width']) / float(data['original_image']['height'])
    return req_ar / orig_ar if req_ar < orig_ar else orig_ar / req_ar
