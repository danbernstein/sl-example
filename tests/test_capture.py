"""

Tests for capturing images from various image sources.

"""

import numpy as np
import cv2

from capture.scrape import capture_img_feed, capture_video_feed


def test_capture_video() -> None:
    """
    test the video capture function.
    :return: None
    """

    url = 'rtmp:/itsvideo.arlingtonva.us:8001/live/cam43.stream'
    feed = cv2.VideoCapture(url)

    img, start_time = capture_video_feed(feed=feed)

    assert type(img) == np.ndarray
    assert type(start_time) == str


def test_capture_image() -> None:
    """
    test the image capture function.
    :return: None
    """

    url = 'http://207.251.86.238/cctv611.jpg'
    img, start_time = capture_img_feed(feed=url)

    assert type(img) == np.ndarray
    assert type(start_time) == str
