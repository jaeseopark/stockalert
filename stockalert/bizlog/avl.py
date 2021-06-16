from collections import defaultdict
from typing import List

from entity.sku import Sku, AvailableSku
from retailerclient.bbclient import BestBuyClient

bbclient = BestBuyClient()


class SkuLookupFactory:
    registry = [
        (lambda retailer: retailer == "bestbuy.ca", bbclient.filter_by_availability,),
    ]

    def get_lookup_handler(retailer):
        for cond, handler in SkuLookupFactory.registry:
            if cond(retailer):
                return handler

        raise RuntimeError(f"No handler found for retailer={retailer}")


def filter_by_availability(skus: List[Sku]) -> List[AvailableSku]:
    skus_by_retailer = defaultdict(list)
    for sku in skus:
        skus_by_retailer[sku.retailer].append(sku)

    available_skus = list()
    for retailer, skus in skus_by_retailer.items():
        # TODO: multi thread
        handler = SkuLookupFactory.get_lookup_handler(retailer)
        available_skus += handler(skus)

    return available_skus
