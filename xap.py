from miio import airpurifier_miot, airpurifier


class Aqi:
    def __init__(self, size):
        self.size = size
        self.items = self.initialize()

    def initialize(self):
        items = []
        for x in range(0, self.size):
            items.append(0)
        return items

    def enqueue(self, item):
        self.items = self.items[: self.size - 1]
        self.items.insert(0, item)

    def is_lower(self, value):
        for x in range(0, self.size):
            if self.items[x] > value:
                return False
        return True

    def is_higher(self, value):
        for x in range(0, self.size):
            if self.items[x] < value:
                return False
        return True


class xap2(airpurifier.AirPurifier):
    def get_aqi(self):
        return self.status().aqi

    def night_mode(self):
        mode = airpurifier.OperationMode("silent")
        self.set_mode(mode)

    def manual_mode(self, level):
        """
        levels
        0: 2-3 m2 (silent,night mode)
        1: 5-9 m2
        2: 8-13 m2
        4: 11-18 m2
        6: 14-24 m2
        8: 17-29 m2
        10: 19-32 m2
        12: 20-25 m2
        14: 22-38 m2
        """
        self.set_favorite_level(level)
        mode = airpurifier.OperationMode("favorite")
        self.set_mode(mode)


class xap3(airpurifier_miot.AirPurifierMiot):
    def get_aqi(self):
        return self.status().aqi

    def night_mode(self):
        mode = airpurifier_miot.OperationMode("silent")
        self.set_mode(mode)

    def manual_mode(self, level):
        """
        levels
        0: 2-3 m2 (silent,night mode)
        1: 5-9 m2
        2: 8-13 m2
        4: 11-18 m2
        6: 14-24 m2
        8: 17-29 m2
        10: 19-32 m2
        12: 20-25 m2
        14: 22-38 m2
        """
        self.set_favorite_level(level)
        mode = airpurifier_miot.OperationMode(2)  # 2 = "favorite"
        self.set_mode(mode)
