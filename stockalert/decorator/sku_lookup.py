from typing import Callable, List

from entity.sku import Sku, AvailableSku
from factory.sku_lookup_factory import SkuLookupFactory


def _no_op(*args, **kwargs):
    return []


def sku_lookup(retailer: str, skip=False):
    def wrapper(func: Callable[[List[Sku]], List[AvailableSku]]):
        if skip:
            func = _no_op
        SkuLookupFactory.register_lookup_handler(retailer, func)
        return func

    return wrapper
