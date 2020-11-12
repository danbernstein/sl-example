import json
import uuid
import os
import traceback
from botocore.exceptions import ClientError
from loguru import logger

from sqsextended.SQSClientExtended import SQSClientExtended
from pysqs_extended_client.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)

BUCKET_NAME = json.loads(os.getenv('data'))['sqs_bucket']
REGION_NAME = 'us-east-1'

sqs = SQSClientExtended(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME,
                        BUCKET_NAME)


def queue_img(data: dict, queue_url: str) -> dict:
    """
    format the captured video frame into a payload and send to queue.

    :param data: payload, including encoded imaged, timestamp, and request metadata.
    :param queue_url: the AWS SQS queue url to send the image to.
    :return: the response from the SQS send message API.
    """
    try:
        payload = {
            'img': data['img'],
            'timestamp': float(data['start_time']),
            'src': data['src'],
            'request_id': data['request_id'],
            'height': data['height'],
            'width': data['width']
        }

        payload_bytes = json.dumps(payload)

        message_group_id = str(uuid.uuid4())
        message_deduplication_id = f"{data['request_id']}-{data['start_time']}"

        response = sqs.send_message(
            queue_url=queue_url,
            message=payload_bytes,
            message_group_id=message_group_id,
            message_deduplication_id=message_deduplication_id,
        )
        return response
    except ClientError:
        logger.error(traceback.format_exc())
        raise
    except Exception as err:
        logger.critical(f'Other error: {err}')
        raise
