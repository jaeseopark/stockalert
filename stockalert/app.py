import csv
import logging
from functools import reduce
from typing import List

from bizlog.sku_filter import by_availability, by_price
from bizlog.ntf import notify
from entity.sku import Sku
from lambdahelper import lambdalogger

lambdalogger.configure()
logger = logging.getLogger(__name__)


def read_local_skus() -> List[Sku]:
    with open("skus.csv", encoding='utf-8') as csvf:
        return [Sku(x) for x in csv.DictReader(csvf)]


def apply(param, func):
    return func(param)


def lambda_handler(event=None, context=None):
    try:
        local_skus = read_local_skus()
        filters = [by_availability, by_price]
        available_skus = reduce(apply, filters, local_skus)
        
        if available_skus:
            notify(available_skus)

        return {
            "statusCode": 200 if available_skus else 204,
            "body": str(available_skus)
        }
    except:
        logger.exception("")
        raise


if __name__ == '__main__':
    lambda_handler()
