# import requests
import logging

from stockalert.bbclient import BestBuyClient
from stockalert.ntf import notify
import lambdalogger

lambdalogger.configure()
logger = logging.getLogger(__name__)

bbclient = BestBuyClient()

# TODO: move the SKUs to a database.
SKUS_TO_MONITOR = ['14950588', '14953247', '14953248', '14953249', '14953250', '14954116', '14954117', '14966477',
                   '14967857', '15000077', '15000078', '15000079', '15038016', '15053085', '15053087', '15078017',
                   '15084753', '15147122', '15166285', '15178453', '15201200', '15229237', '15268899', '15309503',
                   '15309504', '15309513', '15309514', '15317226', '15318940', '15324508', '15373182', '15441686',
                   '15463567', '15463568', '15493494', '15507363', '15524483', '15524484', '15524485', '15530045']


def lambda_handler(event=None, context=None):
    try:
        available_items = bbclient.get_available_items(*SKUS_TO_MONITOR)

        if available_items:
            notify(available_items)

        return {
            "statusCode": 200 if available_items else 204,
            "body": available_items
        }
    except:
        logger.exception("")
        raise
