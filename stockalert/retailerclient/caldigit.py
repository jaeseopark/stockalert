import logging
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from decorator.sku_lookup import sku_lookup
from entity.sku import Sku, AvailableSku
from util.urlstring import get_query_param

from util.network import BROWSER_USER_AGENT

logger = logging.getLogger(__name__)


def to_numeric_price(price_string: str) -> float:
    return float("".join([c for c in price_string if c == "." or c.isnumeric()]))


def to_product_object(soup_element) -> dict:
    link = soup_element.attrs["href"]
    return {
        "product_id": get_query_param(link, "product_id"),
        "price": to_numeric_price(soup_element.find("p", class_="price").text),
        "available": "out of stock" not in soup_element.find("div", class_="caption").text.lower(),
        "link": link
    }


def get_product_map(url: str) -> Dict[str, dict]:
    r = requests.get(url, headers={"user-agent": BROWSER_USER_AGENT})

    if not r.ok:
        logger.error("GET call failed")
        return {}

    soup = BeautifulSoup(r.text, "html.parser")
    products = soup.find_all("a", class_="product-thumb")

    if len(products) == 0:
        logger.info("No product thumbnails found")
        return {}

    return {
        p["product_id"]: p for p in [to_product_object(p) for p in products]
    }


def _filter_by_availability(skus: List[Sku], url: str) -> List[AvailableSku]:
    try:
        product_map = get_product_map(url)
    except:
        # get_product_map() is pretty brittle. expect to fail at any point.
        logger.exception("")
        return []

    available_product_map = {k: v for k, v in product_map.items() if v.get("available")}

    def merge(sku: Sku, product: dict) -> AvailableSku:
        def stringify(_):
            return product.get("link")

        return AvailableSku(sku, price=product.get("price"), stringify=stringify)

    return [
        merge(sku, available_product_map[sku.identifier])
        for sku in skus
        if sku.identifier in available_product_map
    ]


@sku_lookup(retailer="caldigit/docks")
def filter_docks(skus: List[Sku]) -> List[AvailableSku]:
    url = "http://shop.caldigit.com/us/Docking%20Stations"
    return _filter_by_availability(skus, url)


@sku_lookup(retailer="caldigit/refurb")
def filter_refurb(skus: List[Sku]) -> List[AvailableSku]:
    url = "http://shop.caldigit.com/us/index.php?route=product/category&path=88"
    return _filter_by_availability(skus, url)
