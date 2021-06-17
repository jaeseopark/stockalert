import logging
import os
from typing import List

import boto3

from entity.sku import AvailableSku

MAX_SKUS_PER_NOTIFICATION = 1

logger = logging.getLogger(__name__)

snsarn = os.getenv("NOTIFY_SNS_ARN")
snsclient = boto3.client('sns')


def chunks(lst, n):
    """
    Yield successive n-sized chunks from lst.
    https://stackoverflow.com/a/312464
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def notify(available_skus: List[AvailableSku]):
    """
    Sends an SNS notification
    :param available_skus:
    :return:
    """

    for chunk in chunks(available_skus, MAX_SKUS_PER_NOTIFICATION):
        msg = " ".join([str(sku) for sku in chunk])
        response = snsclient.publish(Message=msg, TopicArn=snsarn)
        message_id = response['MessageId']
        logger.info("Published message %s to topic %s.", message_id, snsarn)
