from model.city import City


class CityViewer:
    def __init__(self, city: City) -> None:
        self.city = city

    def draw(self, window):
        print(self.city.intersections)
