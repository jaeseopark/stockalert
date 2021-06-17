from collections import defaultdict
from typing import List

from decorator.sku_lookup import SkuLookupFactory
from entity.sku import Sku, AvailableSku
from util import importdir

# This line imports all modules in the specified directory. This triggers SkuLookupFactory to self-populate.
importdir.do("retailerclient", globals())


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
