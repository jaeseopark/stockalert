import logging

from bs4 import BeautifulSoup

from typing import List

import requests

from decorator.sku_lookup import sku_lookup
from entity.sku import Sku, AvailableSku

from util.network import BROWSER_USER_AGENT

logger = logging.getLogger(__name__)

API_TIMEOUT = 3  # In seconds

HEADERS = {"user-agent": BROWSER_USER_AGENT}


def process_single_sku(sku: Sku) -> AvailableSku:
    url = get_memory_express_product_link(sku)

    logger.info("Making a GET call...")

    r = requests.get(url, headers=HEADERS, timeout=API_TIMEOUT)
    if (not r.ok):
        logger.info(f"Request to memory express url {url} failed with code {r.status_code}")
        return None

    logger.info("GET call was successful")

    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    stores = soup.find_all("div", class_="c-capr-inventory-store")
    if len(stores) > 0:
        for store in stores:
            text = store.text
            if ("Edmonton" in text and "Out" not in text):
                return AvailableSku(sku, link=get_memory_express_product_link(sku))
    else:
        logger.info("Memory express changed their store classname! Please update the store/stock query")

    return None


def lookup(skus: List[Sku]) -> List[AvailableSku]:
    availabilities = []

    for sku in skus:
        available_sku = process_single_sku(sku)
        if available_sku:
            availabilities.append(available_sku)

    logger.info(f"len(availabilities)={len(availabilities)}")

    return availabilities


def get_memory_express_product_link(sku: Sku) -> str:
    return f"https://www.memoryexpress.com/Products/{sku.identifier}"


@sku_lookup(retailer="memoryexpress.com")
def filter_by_availability(skus: List[Sku]) -> List[AvailableSku]:
    return lookup(skus)
