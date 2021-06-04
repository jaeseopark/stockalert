# import requests
from stockalert.bbclient import BestBuyClient
from stockalert.ntf import notify

bbclient = BestBuyClient()

# TODO: move the SKUs to a database.
SKUS_TO_MONITOR = [
    "15078017",
    "15166285"
]


def lambda_handler(event=None, context=None):
    available_items = bbclient.get_available_items(*SKUS_TO_MONITOR)

    if available_items:
        notify(available_items)

    return {
        "status": 200 if available_items else 204,
        "body": available_items
    }
