"""Pic Uploader Engine"""
from PIL import Image
import datetime
from RamWebServiceApp.logger.logger import Logger

from RamWebServiceApp.utils import utils
from RamWebServiceApp.picuploaderengine.uploader_image_profile import ImageUpload

__author__ = 'Ramachandra Raju S'

logger = Logger()


class PicEngine(object):

    """This class will save the profile image to amazon S3."""

    def invoke_engine(self, image_file, file_type, uuid, path, image_type=''):
        """ This method will invoke the photo upload engine
        Functions are verification of the file, file size,
        converting file to jpeg
        """
        logger.Ram_logger('INFO', "TIMING : userpost image - Pic engine start - _" + str(datetime.datetime.now()))
        public_url = None
        random_num = utils.generate_random_number()
        validate_image = ImageValidation(image_file, path)
        logger.Ram_logger('INFO', "TIMING : userpost image - Pic engine finished validation - _" + str(datetime.datetime.now()))
        if validate_image.valid:
            new_loc = path
            # converting image to JPEG
            jpeg_file = self._convert_to_jpeg(path, new_loc)
            logger.Ram_logger('INFO', "TIMING : userpost image - Conversion to jpeg done - _" + str(datetime.datetime.now()))
            if image_type not in ['post_image', 'ask_image', 'give_image','reply_image']:
                logger.Ram_logger('INFO', "PROFILE IMAGE _" + str(datetime.datetime.now()))
                triplication_paths = self._triplicate_image(jpeg_file)
                count = 3
                for path in triplication_paths:
                    end_string = '_original'
                    if count > 1:
                        end_string = '_thumbnail' + str(count)
                        count = count - 1
                    if not image_type:
                        image_type = 'original'
                        logger.Ram_logger('INFO', "TIMING : userpost image - Pic engine entering upload - _" + str(datetime.datetime.now()))
                    public_url = self._upload_file(
                        path, uuid, end_string, random_num, image_type)
            else:
                logger.Ram_logger('INFO', "POST IMAGE _" + str(datetime.datetime.now()))
                public_url = self._upload_file(
                        path, uuid, '_original', random_num, image_type)
            return public_url

        else:
            return validate_image.error

    @staticmethod
    def _upload_file(jpeg_file, uuid, end_string, random_num, image_type):
        """This method will invoke upload  file to amazon S3"""
        logger.Ram_logger('INFO', "-------Start Upload------------" + str(datetime.datetime.now()))
        upload_image = ImageUpload()
        public_url = upload_image.upload_image(
            jpeg_file, uuid, end_string, random_num, image_type)
        logger.Ram_logger('INFO', "-------stop Upload------------" + str(datetime.datetime.now()))
        return public_url

    @staticmethod
    def _triplicate_image(jpeg_file):
        """Triplicate image for thumbnails"""
        logger.Ram_logger('INFO', "TIMING : userpost image - Pic engine start trplicate - _" + str(datetime.datetime.now()))
        original = Image.open(jpeg_file)
        # get different sizes, these should be moved to configuration later
        width, height = original.size
        width1, width2 = width / 4, width / 16
        height1, height2 = height / 4, height / 16

        # building new path
        new_path_list = jpeg_file.split('.')

        resize1_path = new_path_list[0] + '_1.' + new_path_list[1]
        resize2_path = new_path_list[0] + '_2.' + new_path_list[1]

        resize_1 = original.resize((width1, height1), Image.ANTIALIAS)
        resize_1.save(resize1_path)

        resize_2 = original.resize((width2, height2), Image.ANTIALIAS)
        resize_2.save(resize2_path)
        logger.Ram_logger('INFO', "TIMING : userpost image - Pic engine stop triplicate - _" + str(datetime.datetime.now()))

        return resize1_path, resize2_path, jpeg_file

    @staticmethod
    def _convert_to_jpeg(current_file, jpeg_file):
        """ Converting the images to jpeg format """
        image = Image.open(current_file)
        image.save(jpeg_file)
        return jpeg_file


class ImageValidation(object):

    """ Class holding all validation methods for the images, Also compressing
    and converting to jpeg
    """

    def __init__(self, image_file, path):
        self.image = image_file
        self.path = path
        self.error = None
        self.valid = True
        self.validator()

    def validator(self):
        """This validates"""
        # Verifying the file
        if self._check_image_data():
            # checking file format
            if self._check_image_type():
                # Verifying image size
                if self._check_image_size():
                    self.valid = True
                else:
                    self.error = 'size_limit'
            else:
                self.error = 'invalid_format'
        else:
            self.error = 'invalid_file'

    def _check_image_data(self):
        """ Verifies the file image file. """
        try:
            self.image = Image.open(self.path)
            self.image.verify()
        except IOError:
            return False
        return True

    def _check_image_size(self):
        """Verifies image size"""
        import os
        file_size = os.stat(self.path).st_size
        if file_size > 4323200:
            return False
        else:
            return True

    def _check_image_type(self):
        """ Verifies image format JPEG, PNG """
        try:
            file_format = self.image.format
            if file_format in ('JPEG', 'PNG'):
                return True
            else:
                return False
        except IOError:
            return False
