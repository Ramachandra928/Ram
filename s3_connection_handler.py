"""Amazon S3 connection handler"""

import boto
from RamWebService.settings import IMAGE_RESOURCE, S3_REGION_HOST

__author__ = 'Ramachandra Raju S'


class S3ConnectionHandler(object):

    """
    Class will establish and disconnect the connection with Amazon S3
    """

    def open_connect_s3(self):
        """
        Connecti with Amazon S3
        """
        # connect to the bucket
        access_id = IMAGE_RESOURCE["profile_image"]["AWS_ACCESS_KEY_ID"]
        secret_id = IMAGE_RESOURCE["profile_image"]["AWS_SECRET_ACCESS_KEY"]
        kwargs = {

        }
        if S3_REGION_HOST:
            kwargs['host'] = S3_REGION_HOST
        boto.logging.getLogger('boto').setLevel(boto.logging.CRITICAL)
        connection = boto.connect_s3(
            access_id, secret_id, **kwargs)
        return connection

    def close_connect_s3(self, connection):
        """
        Disconnects amazon S3 connection
        """
        connection.close()
