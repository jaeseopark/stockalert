import json
import logging
from bs4 import BeautifulSoup

from typing import List

import requests

from decorator.sku_lookup import sku_lookup
from entity.sku import Sku, AvailableSku

logger = logging.getLogger(__name__)

API_TIMEOUT = 20  # In seconds

def lookup(skus: List[Sku]) -> List[AvailableSku]:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    }

    availabilities = []

    for sku in skus:
        url = get_memory_express_product_link(sku)

        logger.info("Making a GET call...")

        r = requests.get(url, headers=headers, timeout=API_TIMEOUT)
        r.raise_for_status()

        logger.info("GET call was successful")

        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        stores = soup.find_all("div", class_="c-capr-inventory-store")
        for store in stores:
            text = store.text
            if ("Edmonton" in text and "Out" not in text):
                availabilities.append(AvailableSku(sku, stringify=get_memory_express_product_link))
                break

    logger.info(f"len(availabilities)={len(availabilities)}")

    return availabilities


def get_memory_express_product_link(sku: Sku) -> str:
    return f"https://www.memoryexpress.com/Products/{sku.identifier}"


@sku_lookup(retailer="memoryexpress.com")
def filter_by_availability(skus: List[Sku]) -> List[AvailableSku]:
    sku_dict: dict = {sku.identifier: sku for sku in skus}
    availabilities = lookup(skus)
    return availabilities
