import logging
import os
from collections import defaultdict
from typing import List, Dict

import boto3

from entity.sku import AvailableSku

from util.array import chunks

MAX_SKUS_PER_NOTIFICATION = 1

logger = logging.getLogger(__name__)

snsarn = os.getenv("NOTIFY_SNS_ARN")
snsclient = boto3.client('sns')


def group_by_discord(available_skus: List[AvailableSku]) -> Dict[str, List[AvailableSku]]:
    groupped = defaultdict(list)
    for asku in available_skus:
        groupped[asku.discord] = asku
    return groupped


def to_sns_message(discord: str, skus: List[AvailableSku]) -> str:
    concat_skus = " ".join([str(sku) for sku in skus])
    return f"{discord},{concat_skus}"


def notify(available_skus: List[AvailableSku]):
    """
    Sends an SNS notification
    :param available_skus:
    :return:
    """

    groupped = group_by_discord(available_skus)

    for discord, skus in groupped.items():
        for chunk in chunks(available_skus, MAX_SKUS_PER_NOTIFICATION):
            message = to_sns_message(discord, chunk)
            response = snsclient.publish(Message=message, TopicArn=snsarn)
            message_id = response['MessageId']
            logger.info("Published message %s to topic %s.", message_id, snsarn)
