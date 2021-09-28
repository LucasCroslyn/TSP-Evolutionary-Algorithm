class City:
    def __init__(self, name, cityId, distances):
        self.name = name
        self.cityId = cityId
        self.distances = distances

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name