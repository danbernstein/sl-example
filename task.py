"""
The script captures a video frame from the feed based on the feed data format
and sends the encoded image and relevant metadata to an AWS first-in-first-out (FIFO) SQS queue to be
processed in order received. Using a FIFO queue allows frames to be processed in order, so object tracking is possible.

The script uses the sqsextended module (https://github.com/timothymugayi/boto3-sqs-extended-client-lib.git) to link SQS messages to the encoded image which
is stored as an S3 object. Images in their raw format and dimensions are too large to meet the SQS 256 kilobyte message body limit.

"""
import time
import os
import json
import traceback
import base64
import cv2
from loguru import logger

from capture.scrape import capture_video_feed, capture_img_feed, make_capture_obj

LOCAL = True

if not LOCAL:
    from capture.aws.sqs import queue_img


if LOCAL:
    os.environ['AWS_ACCESS_KEY_ID'] = 'dummy_aws_access_key_id'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'dummy_aws_secret_access_key'
    os.environ['data'] = '{"queue_url": "dummy_queue", "src": "rtmp:/itsvideo.arlingtonva.us:8001/live/cam43.stream", "sleep": 0.5,     "request_id": "dummy_request_id", "sqs_bucket": "dummy_bucket_name"}'


def stream_feed(data: dict) -> None:
    """
    Main function for capturing video feed data. This function will continue running until the container is terminated
    because exceptions are logged and passed.

    :param data: request information as a dictionary, including camera and request metadata.
    :returns: None. Output is sent to the queue for processing by the other container. The response from the call to AWS SQS is logged.

    """

    cap = make_capture_obj(data['src'])

    output = data.copy()

    counter = 0
    while counter < 10:
        try:
            if cap:
                frame, output['start_time'] = capture_video_feed(feed=cap)
            else:
                frame, output['start_time'] = capture_img_feed(
                    feed=data['src'])

            output['height'], output['width'], channels = frame.shape
            _, img_encoded = cv2.imencode('.jpg', frame)

            output['img'] = base64.b64encode(img_encoded).decode()

            if LOCAL:
                img_file = f'frame_{counter}.jpg'
                cv2.imwrite(img_file, frame)
                response = f'frame captured from {output["src"]} and saved to {img_file}'
            else:
                response = queue_img(data=output,
                                     queue_url=output['queue_url'])

            logger.info(response)
            time.sleep(data['sleep'])
            counter += 1
        except AttributeError:
            # re-establish video capture if 'NoneType' error occurs because the connection has been dropped.
            logger.error(
                f"re-establishing video connection with {data['src']}")
            cap = make_capture_obj(data['src'])
        except:
            logger.error(traceback.format_exc())
            continue


if __name__ == '__main__':
    """entry point"""
    try:
        data = json.loads(os.getenv('data'))
        logger.info(f'received data: {data}')
    except TypeError as e:
        logger.error('no environmental variables available')
        raise

    stream_feed(data)
