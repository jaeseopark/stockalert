import json
import logging
from typing import List

import requests

from decorator.sku_lookup import sku_lookup
from entity.sku import Sku, AvailableSku

logger = logging.getLogger(__name__)

OUT_OF_STOCK_STATUS_LIST = [None, "NotAvailable", "ComingSoon", "SoldOutOnline"]
API_TIMEOUT = 20  # In seconds


def is_available(bb_api_res: dict):
    shipping = bb_api_res.get("shipping")
    status = shipping and shipping.get("status")
    purchasable = shipping and shipping.get("purchasable")  # is this useful?
    return purchasable or status not in OUT_OF_STOCK_STATUS_LIST


def lookup(skus: List[Sku]) -> List[dict]:
    joined_skus = "|".join([i.identifier for i in skus])
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
    availabilities = data.get("availabilities", list())

    logger.info(f"len(availabilities)={len(availabilities)}")

    return availabilities


def get_bb_product_link(sku: Sku) -> str:
    return f"https://www.bestbuy.ca/en-ca/product/{sku.identifier}"


@sku_lookup(retailer="bestbuy.ca")
def filter_by_availability(skus: List[Sku]) -> List[AvailableSku]:
    sku_dict: dict = {sku.identifier: sku for sku in skus}
    availabilities = lookup(skus)

    return [AvailableSku(sku_dict[x["sku"]], stringify=get_bb_product_link)
            for x in availabilities
            if is_available(x)]
