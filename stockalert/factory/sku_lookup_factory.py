from typing import List, Mapping, Callable

from entity.sku import Sku, AvailableSku


class SkuLookupFactory:
    registry: Mapping[str, Callable[[List[Sku]], List[AvailableSku]]] = dict()

    @staticmethod
    def get_lookup_handler(retailer: str) -> Callable[[List[Sku]], List[AvailableSku]]:
        return SkuLookupFactory.registry[retailer]

    @staticmethod
    def register_lookup_handler(retailer: str, func: Callable[[List[Sku]], List[AvailableSku]]):
        assert retailer not in SkuLookupFactory.registry
        SkuLookupFactory.registry[retailer] = func
