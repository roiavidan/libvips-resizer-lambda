import pyvips

def thumbnail(original_image, sz='200x200'):
    image = pyvips.Image.new_from_buffer(original_image, '')
    new_image = image.resize(0.5)
    return new_image.write_to_buffer('.jpg')
