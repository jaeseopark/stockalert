from typing import Callable, List

from entity.sku import Sku, AvailableSku
from factory.sku_lookup_factory import SkuLookupFactory


def sku_lookup(retailer: str):
    def wrapper(func: Callable[[List[Sku]], List[AvailableSku]]):
        SkuLookupFactory.register_lookup_handler(retailer, func)
        return func

    return wrapper
