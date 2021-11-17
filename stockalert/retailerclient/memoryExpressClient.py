import logging
import re
from functools import lru_cache

from bs4 import BeautifulSoup

from typing import List

import requests

from decorator.sku_lookup import sku_lookup
from entity.sku import Sku, AvailableSku

from util.network import BROWSER_USER_AGENT

logger = logging.getLogger(__name__)

API_TIMEOUT = 3  # In seconds

HEADERS = {"user-agent": BROWSER_USER_AGENT}

REGEX_DOLLAR_AMOUNT_SANITIZER = re.compile(r"[^0-9.]")


@lru_cache(maxsize=10)
def get_api_response(url: str):
    logger.info("Making a GET call...")

    r = requests.get(url, headers=HEADERS, timeout=API_TIMEOUT)
    if not r.ok:
        logger.info(f"Request to memory express url {url} failed with code {r.status_code}")
        return None

    logger.info("GET call was successful")

    return r.text


def get_price(soup: BeautifulSoup) -> float:
    divs = soup.find_all("div", class_="c-capr-pricing__grand-total")
    for text in [div.text for div in divs]:
        if "$" in text:
            return float(REGEX_DOLLAR_AMOUNT_SANITIZER.sub("", text))
    return None


def process_single_sku(sku: Sku, region: str) -> AvailableSku:
    url = get_memory_express_product_link(sku)
    html_doc = get_api_response(url)
    soup = BeautifulSoup(html_doc, 'html.parser')

    price = get_price(soup)

    stores = soup.find_all("div", class_="c-capr-inventory-store")
    if len(stores) > 0:
        for store in stores:
            text = store.text
            if region in text and "Out" not in text:
                return AvailableSku(sku, price=price, link=get_memory_express_product_link(sku))
    else:
        logger.info("Memory express changed their store classname! Please update the store/stock query")

    return None


def lookup_by_region(skus: List[Sku], region: str) -> List[AvailableSku]:
    availabilities = []

    for sku in skus:
        available_sku = process_single_sku(sku, region)
        if available_sku:
            availabilities.append(available_sku)

    logger.info(f"len(availabilities)={len(availabilities)}")

    return availabilities


def get_memory_express_product_link(sku: Sku) -> str:
    return f"https://www.memoryexpress.com/Products/{sku.identifier}"


@sku_lookup(retailer="memoryexpress.com/Edmonton")
def filter_by_availability(skus: List[Sku]) -> List[AvailableSku]:
    return lookup_by_region(skus, "Edmonton")


@sku_lookup(retailer="memoryexpress.com/Vancouver")
def filter_by_availability(skus: List[Sku]) -> List[AvailableSku]:
    return lookup_by_region(skus, "Vancouver")
