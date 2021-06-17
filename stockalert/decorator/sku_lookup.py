class SkuLookupFactory:
    registry = dict()

    @staticmethod
    def get_lookup_handler(retailer: str):
        return SkuLookupFactory.registry[retailer]


def sku_lookup(retailer: str):
    def wrapper(func):
        assert retailer not in SkuLookupFactory.registry
        SkuLookupFactory.registry[retailer] = func
        return func

    return wrapper
