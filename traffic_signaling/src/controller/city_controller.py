import math
from model import city


class CityController:
    def __init__(self, city, window_size) -> None:
        self.city = city
        self.time = 0
        self.window_size = window_size
        self.set_intersection_pos()

    def set_intersection_pos(self) -> None:
        intersections_no = len(self.city.intersections)
        center = (self.window_size[0] / 2, self.window_size[1] / 2)
        radius = self.window_size[1] / 2 - 50
        angle = 0
        rotation_angle = (2 * math.pi) / intersections_no
        for id, intersection in self.city.intersections.items():
            intersection.set_pos(center[0] + math.sin(angle)*radius,
                                 center[1] + math.cos(angle)*radius)

            angle += rotation_angle
        return

    def update(self) -> None:
        self.time += 1
