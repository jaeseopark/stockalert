from typing import List

from entity.sku import AvailableSku


def is_acceptable_price(asku: AvailableSku) -> bool:
    if asku.price is not None and asku.price_threshold is not None:
        return asku.price <= asku.price_threshold

    return True


def by_price(available_skus: List[AvailableSku]) -> List[AvailableSku]:
    return [asku for asku in available_skus if is_acceptable_price(asku)]
