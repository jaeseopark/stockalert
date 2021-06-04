import logging
import os

import boto3

MAX_ITEMS_PER_NOTIFICATION = 2

# TODO: add log handler.
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


def get_message(item):
    sku = item["sku"]  # should fail if "sku" does not exist in the dictionary
    return f"https://www.bestbuy.ca/en-ca/product/{sku}"


def notify(available_items):
    """
    Sends an SNS notification
    :param available_items:
    :return:
    """

    attributes = dict()

    for chunk in chunks(available_items, MAX_ITEMS_PER_NOTIFICATION):
        msg = " ".join([get_message(item) for item in chunk])
        response = snsclient.publish(Message=msg, TopicArn=snsarn)
        message_id = response['MessageId']
        logger.info("Published message %s with attributes %s to topic %s.", message_id, attributes, snsarn)
