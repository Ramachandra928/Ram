""" File will deals with the cassandra operations related to pic upload"""

from RamWebServiceApp.userprofile.userprofile_cass import update_scheduler_data_profile
from RamWebService.db import get_connection

__author__ = 'Ramachandra Raju S'


def update_profile_image(uuid, image_url):
    """ This method stores all the profile image's url
    once it has been stored in S3
    """
    session = get_connection()
    add_user_image = session.prepare("""
        INSERT INTO user_profile (guid, profile_image_url)
        VALUES (?, ?)
    """)
    session.execute(add_user_image,
                    (uuid, image_url))
    update_scheduler_data_profile(uuid)


def update_post_image(post_id, event_id, posted_time, post_images):
    """ This method stores post image """
    session = get_connection()
    add_user_image = session.prepare("""
        INSERT INTO posts (post_id, event_id, posted_time, post_images)
        VALUES (?, ?, ?, ?)
    """)
    session.execute(add_user_image,
                    (post_id, event_id, posted_time, post_images))


def update_cover_image(uuid, image_url):
    """ This method stores all the profile image's url
    once it has been stored in S3
    """
    session = get_connection()
    add_user_image = session.prepare("""
        INSERT INTO user_profile (guid, cover_photo_url)
        VALUES (?, ?)
    """)
    session.execute(add_user_image,
                    (uuid, image_url))
    update_scheduler_data_profile(uuid)
