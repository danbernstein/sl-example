"""

Functions for capturing frames from video and image feeds.

"""
import time
import traceback
from typing import Union
from loguru import logger
import cv2
import imutils


def make_capture_obj(src: str) -> Union[cv2.VideoCapture, None]:
    """
    create a cv2 VideoCapture object if the input source is a video format.
    The returned object is required to capture images from a video feed.

    :param src:
    :return: either the cv2 Video Capture object or None.
    """

    if src.rsplit('.', 1)[-1] in ['avi', 'mp4', 'stream']:
        cap = cv2.VideoCapture(src)
    else:
        cap = None

    return cap


def capture_video_feed(feed: cv2.VideoCapture) -> tuple:
    """
    capture image from an video feed.

    :param feed: cv2 VideoCapture object to read images from.
    :return: tuple of the image still and the time captured.
    """
    try:
        start_time = str(float(time.time()))
        ret, frame = feed.read()
        return frame, start_time
    except AttributeError:
        logger.error(f'feed is of incorrect type : {type(feed)}')
        raise
    except:
        logger.error(traceback.format_exc())


def capture_img_feed(feed: str) -> tuple:
    """
    capture image from an image feed.

    :param feed: video url to capture frames from.
    :return: tuple of image still and the captured.
    """
    try:
        start_time = str(float(time.time()))
        frame = imutils.url_to_image(feed)
        return frame, start_time
    except:
        logger.error(traceback.format_exc())
