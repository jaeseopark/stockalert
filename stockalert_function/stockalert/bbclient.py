import json
import logging

import requests

logger = logging.getLogger(__name__)

OUT_OF_STOCK_STATUS_LIST = [None, "NotAvailable", "ComingSoon", "SoldOutOnline"]
API_TIMEOUT = 20  # In seconds


def is_available(item):
    shipping = item.get("shipping")
    status = shipping and shipping.get("status")
    purchasable = shipping and shipping.get("purchasable")  # is this useful?
    if status not in OUT_OF_STOCK_STATUS_LIST or purchasable:
        return True

    return False


def lookup(*skus):
    joined_skus = "|".join(skus)
    url = f"https://www.bestbuy.ca/ecomm-api/availability/products?skus={joined_skus}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    }

    logger.info("Making a GET call...")

    r = requests.get(url, headers=headers, timeout=API_TIMEOUT)
    r.raise_for_status()

    logger.info("GET call was successful")

    decoded_data = r.text.encode().decode('utf-8-sig')
    data = json.loads(decoded_data)
    items = data.get("availabilities", list())

    logger.info(f"len(items)={len(items)}")

    return items


class BestBuyClient:
    def get_available_items(self, *skus):
        data = lookup(*skus)
        return [x for x in data if is_available(x)]
