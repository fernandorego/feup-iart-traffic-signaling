from model import city


class CityController:
    def __init__(self, city) -> None:
        self.city = city
        self.time = 0
        self.set_intersection_pos()

    def set_intersection_pos(self) -> None:
        # TODO: setup intersection position for pygame
        return

    def update(self):
        self.time += 1
