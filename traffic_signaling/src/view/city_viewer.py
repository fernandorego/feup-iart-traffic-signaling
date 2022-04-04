import pygame
from math import atan2, degrees, radians, cos, sin, dist
from model.city import City

INTERSECTION_COLOR = (85, 156, 173)
TEXT_COLOR = (50, 50, 50)
BLOCKSIZE = 30
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class CityViewer:
    def __init__(self, city: City) -> None:
        self.city = city
        self.streets = self.get_roads()
        print(self.streets)

    def get_roads(self):
        streets = []

        for id1, intersection1 in self.city.intersections.items():
            for outcoming in intersection1.outgoing_streets:
                st = False
                for id2, intersection2 in self.city.intersections.items():
                    for incoming in intersection2.incoming_streets:
                        if (outcoming.id == incoming.id):
                            streets.append((outcoming.id, id1, id2))
                            st = True
                            break
                    if st:
                        break

        return streets

    def draw(self, window) -> None:
        for street in self.streets:
            self.draw_road(window, street)

        font = pygame.font.SysFont(None, 24)

        for id, intersection in self.city.intersections.items():
            self.draw_intersection(window, id, intersection, font)

    def draw_road(self, window, street):
        start_intersect_pos = self.city.intersections[street[1]].get_pos()
        end_intersect_pos = self.city.intersections[street[2]].get_pos()

        angle = degrees(atan2(end_intersect_pos[1] - start_intersect_pos[1],
                              end_intersect_pos[0] - start_intersect_pos[0]))

        road_block = pygame.image.load(
            '../asset/img/road.png').convert_alpha()
        road_block = pygame.transform.scale(
            road_block, (BLOCKSIZE, BLOCKSIZE))
        road_block = pygame.transform.rotate(road_block, -angle)

        pos = start_intersect_pos

        distance = dist(pos, end_intersect_pos)

        while (dist(pos, end_intersect_pos) <= distance):
            distance = dist(pos, end_intersect_pos)
            rotated_center = (road_block.get_rect(
                center=(pos[0], pos[1])))
            window.blit(road_block, rotated_center)

            pos = (pos[0] + BLOCKSIZE*cos(radians(angle)),
                   pos[1] + BLOCKSIZE*sin(radians(angle)))

    def draw_intersection(self, window, id, intersection, font):
        pygame.draw.circle(window, INTERSECTION_COLOR,
                           intersection.get_pos(), 35.0)
        img = font.render(str(id), True, TEXT_COLOR)
        window.blit(img, (intersection.get_pos()[0] - 5,
                          intersection.get_pos()[1] - 7))
