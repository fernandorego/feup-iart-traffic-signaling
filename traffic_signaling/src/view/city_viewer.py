import pygame
from math import atan2, degrees, radians, cos, sin, dist
from model.city import City

INTERSECTION_COLOR = (194, 146, 74)
INTERSECTION_SIZE = 45
FONT_SIZE = 24
TEXT_COLOR = (50, 50, 50)
BLOCKSIZE = 40
CAR_LEN = 40
CAR_WIDTH = 30
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_OFFSET = 70
CAR_OFFSET = 1.8

ROAD_IMAGE = '../asset/img/road.png'
CAR_IMAGE = '../asset/img/car.png'
GREEN_LIGHT_IMAGE = '../asset/img/green.png'
RED_LIGHT_IMAGE = '../asset/img/red.png'


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

            for id, info in cars_position.items():
                if info[0] == street[0]:
                    self.draw_car(window, street, info[1])

        font = pygame.font.SysFont(None, FONT_SIZE)

        for id, intersection in self.city.intersections.items():
            self.draw_intersection(window, id, intersection, font)

    def draw_road(self, window, street, green):
        start_intersect_pos = self.city.intersections[street[1]].get_pos()
        end_intersect_pos = self.city.intersections[street[2]].get_pos()

        angle = degrees(atan2(end_intersect_pos[1] - start_intersect_pos[1],
                              end_intersect_pos[0] - start_intersect_pos[0]))

        road_block, green_block, red_block = self.load_blocks(angle)

        pos = start_intersect_pos

        distance = dist(pos, end_intersect_pos)

        while (dist(pos, end_intersect_pos) <= distance):
            distance = dist(pos, end_intersect_pos)
            if green and distance < LIGHT_OFFSET:
                rotated_center = (green_block.get_rect(
                    center=(pos[0], pos[1])))
                window.blit(green_block, rotated_center)
            elif not green and distance < LIGHT_OFFSET:
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

        angle = atan2(end_intersect_pos[1] - start_intersect_pos[1],
                      end_intersect_pos[0] - start_intersect_pos[0])

        distance = dist(start_intersect_pos, end_intersect_pos) / street[4]

        if l == 0:
            pos = (start_intersect_pos[0] + round(street[4] * distance * cos(angle) - CAR_OFFSET * BLOCKSIZE * cos(angle)),
                   start_intersect_pos[1] + round(street[4] * distance * sin(angle) - CAR_OFFSET * BLOCKSIZE * sin(angle)))
        else:
            pos = (start_intersect_pos[0] + round((street[4] - l) * distance * cos(angle) - 0.5 * distance * cos(angle)),
                   start_intersect_pos[1] + round((street[4] - l) * distance * sin(angle) - 0.5 * distance * sin(angle)))

        car = self.load_car(angle)

        rotated_center = (car.get_rect(
            center=(pos[0], pos[1])))
        window.blit(car, rotated_center)

    def draw_intersection(self, window, id, intersection, font):
        pygame.draw.circle(window, INTERSECTION_COLOR,
                           intersection.get_pos(), INTERSECTION_SIZE)
        img = font.render(str(id), True, TEXT_COLOR)
        pos = intersection.get_pos()
        window.blit(img, (pos[0] - 5, pos[1] - 7))

    def load_blocks(self, angle):
        green_block = pygame.image.load(GREEN_LIGHT_IMAGE).convert_alpha()
        green_block = pygame.transform.scale(
            green_block, (BLOCKSIZE, BLOCKSIZE))

        red_block = pygame.image.load(RED_LIGHT_IMAGE).convert_alpha()
        red_block = pygame.transform.scale(
            red_block, (BLOCKSIZE, BLOCKSIZE))

        road_block = pygame.image.load(ROAD_IMAGE).convert_alpha()
        road_block = pygame.transform.scale(
            road_block, (BLOCKSIZE, BLOCKSIZE))

        return (pygame.transform.rotate(road_block, -angle),
                pygame.transform.rotate(green_block, -angle),
                pygame.transform.rotate(red_block, -angle))

    def load_car(self, angle):
        car = pygame.image.load(CAR_IMAGE).convert_alpha()
        car = pygame.transform.scale(
            car, (CAR_LEN, CAR_WIDTH))
        return pygame.transform.rotate(car, -degrees(angle))
