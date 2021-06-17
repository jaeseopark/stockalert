import csv
import logging
from typing import List

from bizlog.avl import filter_by_availability
from bizlog.ntf import notify
from entity.sku import Sku
from lambdahelper import lambdalogger

lambdalogger.configure()
logger = logging.getLogger(__name__)


def get_skus_to_monitor() -> List[Sku]:
    with open("skus.csv", encoding='utf-8') as csvf:
        return [Sku(x) for x in csv.DictReader(csvf)]


def lambda_handler(event=None, context=None):
    try:
        skus = get_skus_to_monitor()
        available_skus = filter_by_availability(skus)

        if available_skus:
            notify(available_skus)

        return {
            "statusCode": 200 if available_skus else 204,
            "body": available_skus
        }
    except:
        logger.exception("")
        raise


if __name__ == '__main__':
    lambda_handler()
