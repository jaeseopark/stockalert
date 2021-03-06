class Sku:
    def __init__(self, *init, **kwargs):
        self.discord = None
        self.retailer = None
        self.identifier = None
        self.shortname = None
        self.name = None
        self.price_threshold = None

        for dictionary in init:
            if isinstance(dictionary, Sku):
                dictionary = dictionary.__dict__
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class AvailableSku(Sku):
    def __init__(self, *init, **kwargs):
        self.link = None
        self.price = None
        super(AvailableSku, self).__init__(*init, **kwargs)
        assert self.link is not None

    def __str__(self):
        return f"{self.shortname} {self.link}"

    def __repr__(self):
        return str(self)
