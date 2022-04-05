import pygame
from math import atan2, ceil, degrees, floor, radians, cos, sin, dist
from model.city import City

INTERSECTION_COLOR = (85, 156, 173)
TEXT_COLOR = (50, 50, 50)
BLOCKSIZE = 30
CAR_LEN = 15
CAR_WIDTH = 10
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class CityViewer:
    def __init__(self, city: City) -> None:
        self.city = city
        self.streets = self.get_roads()

    def get_roads(self):
        streets = []

        for id1, intersection1 in self.city.intersections.items():
            for outcoming in intersection1.outgoing_streets:
                st = False
                for id2, intersection2 in self.city.intersections.items():
                    for incoming in intersection2.incoming_streets:
                        if (outcoming.id == incoming.id):
                            streets.append(
                                (outcoming.id, id1, id2, outcoming.name, outcoming.length))
                            st = True
                            break
                    if st:
                        break
        return streets

    def draw(self, window, green_lights_streets, cars_position) -> None:
        for street in self.streets:
            green = street[3] in green_lights_streets
            self.draw_road(window, street, green)
            # if street[0] in cars_position:
            for id, info in cars_position.items():
                if info[0] == street[0]:
                    self.draw_car(window, street, info[1])

        font = pygame.font.SysFont(None, 24)

        for id, intersection in self.city.intersections.items():
            self.draw_intersection(window, id, intersection, font)

    def draw_road(self, window, street, green):
        start_intersect_pos = self.city.intersections[street[1]].get_pos()
        end_intersect_pos = self.city.intersections[street[2]].get_pos()

        angle = degrees(atan2(end_intersect_pos[1] - start_intersect_pos[1],
                              end_intersect_pos[0] - start_intersect_pos[0]))

        green_block = pygame.image.load(
            '../asset/img/green.png').convert_alpha()
        green_block = pygame.transform.scale(
            green_block, (BLOCKSIZE, BLOCKSIZE))
        green_block = pygame.transform.rotate(green_block, -angle)

        red_block = pygame.image.load(
            '../asset/img/red.png').convert_alpha()
        red_block = pygame.transform.scale(
            red_block, (BLOCKSIZE, BLOCKSIZE))
        red_block = pygame.transform.rotate(red_block, -angle)

        road_block = pygame.image.load(
            '../asset/img/road.png').convert_alpha()
        road_block = pygame.transform.scale(
            road_block, (BLOCKSIZE, BLOCKSIZE))
        road_block = pygame.transform.rotate(road_block, -angle)

        pos = start_intersect_pos

        distance = dist(pos, end_intersect_pos)

        while (dist(pos, end_intersect_pos) <= distance):
            distance = dist(pos, end_intersect_pos)
            if green and distance < 50:
                rotated_center = (green_block.get_rect(
                    center=(pos[0], pos[1])))
                window.blit(green_block, rotated_center)
            elif not green and distance < 60:
                rotated_center = (red_block.get_rect(
                    center=(pos[0], pos[1])))
                window.blit(red_block, rotated_center)
            else:
                rotated_center = (road_block.get_rect(
                    center=(pos[0], pos[1])))
                window.blit(road_block, rotated_center)

            pos = (pos[0] + round(BLOCKSIZE*cos(radians(angle))),
                   pos[1] + round(BLOCKSIZE*sin(radians(angle))))

    def draw_car(self, window, street, l):

        start_intersect_pos = self.city.intersections[street[1]].get_pos()
        end_intersect_pos = self.city.intersections[street[2]].get_pos()

        angle = degrees(atan2(end_intersect_pos[1] - start_intersect_pos[1],
                              end_intersect_pos[0] - start_intersect_pos[0]))

        distance = dist(start_intersect_pos, end_intersect_pos) / street[4]

        if l == 0:
            pos = (start_intersect_pos[0] + round(street[4] * distance * cos(radians(angle)) - 1.5 * BLOCKSIZE * cos(radians(angle))),
                   start_intersect_pos[1] + round(street[4] * distance * sin(radians(angle)) - 1.5 * BLOCKSIZE * sin(radians(angle))))
        else:
            pos = (start_intersect_pos[0] + round((street[4] - l) * distance * cos(radians(angle)) - 0.5 * distance * cos(radians(angle))),
                   start_intersect_pos[1] + round((street[4] - l) * distance * sin(radians(angle)) - 0.5 * distance * sin(radians(angle))))

        car = pygame.image.load(
            '../asset/img/car.png').convert_alpha()
        car = pygame.transform.scale(
            car, (CAR_LEN, CAR_WIDTH))
        car = pygame.transform.rotate(car, -angle)

        rotated_center = (car.get_rect(
            center=(pos[0], pos[1])))
        window.blit(car, rotated_center)

    def draw_intersection(self, window, id, intersection, font):
        pygame.draw.circle(window, INTERSECTION_COLOR,
                           intersection.get_pos(), 35.0)
        img = font.render(str(id), True, TEXT_COLOR)
        window.blit(img, (intersection.get_pos()[0] - 5,
                          intersection.get_pos()[1] - 7))
