""" Python file used to getting details for the upload"""

__author__ = 'Ramachandra Raju S'


def get_public_url(host, key):
    """
    This will make the public url for the file
    """
    s3_public_url = 'http://{host}/{key}'.format(
        host=host, key=key)
    return s3_public_url


def get_image_name(uuid, extension, random_num):
    """
    This will create image name
    """
    image_name = None
    image_name = uuid + '_' + str(random_num) + '_' + extension
    return image_name


def get_profile_image_name(uuid, extension):
    """
    This will create image name
    """
    image_name = None
    image_name = uuid + '' + extension
    return image_name
