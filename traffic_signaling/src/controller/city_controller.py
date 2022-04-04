import math
from collections import deque
from time import sleep

import pygame
from model.city import City
from model.schedule import Schedule
from view.city_viewer import CityViewer

BG_COLOR = (200, 200, 200)


class CityController:
    def __init__(self, city: City, schedule: Schedule, window, window_size) -> None:
        self.city = city
        self.city_viewer = CityViewer(city)
        self.schedule = schedule
        self.time = 0
        self.window = window
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

    def evaluate(self):
        # setup simulation helpers
        street_queue = {street_id: deque()
                        for street_id in range(self.city.no_streets)}

        green_cycle_duration = {intersection_id: len(self.schedule.schedule[intersection_id])
                                for intersection_id in self.schedule.schedule}

        car_path = {}
        next_analysed_time = {}
        for car in self.city.cars:
            car_path[car.id] = deque(car.path)
            street_queue[car_path[car.id][0].id].append(car.id)
            next_analysed_time[car.id] = 0

        print()
        print(self.city.street_intersection)
        print(street_queue)
        print(green_cycle_duration)
        print(car_path)
        print(next_analysed_time)
        print()

        # run simulation
        score = 0
        for current_time in range(self.city.duration+1):
            crossed_intersections = []
            scheduled_removals = []
            for car_id in car_path:
                # ainda não chegou a interseção
                if next_analysed_time[car_id] > current_time:
                    continue
                street = car_path[car_id][0]
                if street_queue[car_path[car_id][0].id][0] != car_id:  # primeiro carro da fila
                    continue
                intersection_id = self.city.street_intersection[street.name]
                light_is_green = self.schedule.schedule[intersection_id][current_time %
                                                                         green_cycle_duration[intersection_id]] == street.name
                if not light_is_green or intersection_id in crossed_intersections:
                    continue

                crossed_intersections.append(intersection_id)
                street_queue[street.id].popleft()
                car_path[car_id].popleft()
                next_street = car_path[car_id][0]
                next_time = current_time + next_street.length
                if len(car_path[car_id]) == 1:
                    scheduled_removals.append(car_id)
                    if next_time <= self.city.duration:
                        score += self.city.car_value + self.city.duration - next_time
                else:
                    street_queue[next_street.id].append(car_id)
                    next_analysed_time[car_id] = next_time
            for car_id in scheduled_removals:
                del car_path[car_id]

            print()
            print(street_queue)
            print(green_cycle_duration)
            print(car_path)
            print(next_analysed_time)
            print()

            sleep(1)

        return score

    def draw(self):
        self.window.fill(BG_COLOR)

        self.city_viewer.draw(self.window)

        pygame.display.flip()
