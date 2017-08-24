import base64


PADDED_RECTANGLE = '<rect x="0" y="0" width="100%" height="100%" fill="white" />'


def embed(image_data, data):
    width = data['resized_image']['width']
    height = data['resized_image']['height']
    if data['padding']:
        requested_width = data['requested_image']['width']
        requested_height = data['requested_image']['height']

        # Get offsets so the image will be centered
        x_offset = (requested_width - width) / 2
        y_offset = (requested_height - height) / 2

        # Check if padding is needed
        padded_rectangle = PADDED_RECTANGLE
    else:
        x_offset = y_offset = 0
        padded_rectangle = ''
        requested_width = width
        requested_height = height

    return \
        '<?xml version="1.0" encoding="UTF-8" ?>' \
        '<svg version="1.1" baseProfile="tiny" width="{req_width}" height="{req_height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' \
        '{padded_rectangle}' \
        '<image x="{x_offset}" y="{y_offset}" width="{thumb_width}" height="{thumb_height}" xlink:href="data:image/jpg;base64,{base64_image}" />' \
        '</svg>'.format(thumb_width=width, thumb_height=height,
            req_width=requested_width, req_height=requested_height,
            x_offset=x_offset, y_offset=y_offset,
            padded_rectangle=padded_rectangle, base64_image=base64.b64encode(image_data))
