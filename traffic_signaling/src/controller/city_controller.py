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
            intersection.set_pos(center[0] + math.sin(angle)*radius*1.3,
                                 center[1] + math.cos(angle)*radius)

            angle += rotation_angle
        return

    def simulate(self):
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

        # run simulation
        score = 0
        for current_time in range(self.city.duration + 1):
            crossed_intersections = []
            scheduled_removals = []
            green_lights_streets = []

            for id, intersection in self.schedule.schedule.items():
                green_lights_streets.append(
                    intersection[current_time % green_cycle_duration[id]])

            # {street_id: [street, L]}
            cars_position = {car_id: [car_path[car_id][0].id, max(next_analysed_time[car_id] - current_time, 0)]
                             for car_id in car_path}
            print("TIME=", current_time, "CARS=", cars_position)

            for car_id in car_path:
                if next_analysed_time[car_id] > current_time:
                    continue
                street = car_path[car_id][0]
                if street_queue[street.id][0] != car_id:
                    continue
                intersection_id = self.city.street_intersection[street.name]
                light_is_green = self.schedule.schedule[intersection_id][current_time %
                                                                         green_cycle_duration[intersection_id]] == street.name
                if not light_is_green or intersection_id in crossed_intersections:
                    continue

                crossed_intersections.append(intersection_id)
                street_queue[street.id].popleft()
                car_path[car_id].popleft()

                if len(car_path[car_id]) == 0:
                    scheduled_removals.append(car_id)
                else:
                    next_street = car_path[car_id][0]
                    next_time = current_time + next_street.length
                    street_queue[next_street.id].append(car_id)
                    next_analysed_time[car_id] = next_time
            for car_id in scheduled_removals:
                del car_path[car_id]

            self.draw(green_lights_streets, cars_position)

            sleep(1)

    def draw(self, green_lights, cars_position):
        self.window.fill(BG_COLOR)

        self.city_viewer.draw(self.window, green_lights, cars_position)

        pygame.display.flip()
