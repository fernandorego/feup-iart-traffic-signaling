from time import sleep
from .city import City
import copy


class Schedule:
    def __init__(self):
        self.schedule = dict()

    def from_input(input_file: str):
        with open(input_file) as f:
            lines = f.readlines()
        lines = [line.strip('\n').split(' ') for line in lines]

        schedule = Schedule()
        no_intersections = int(lines[0][0])
        lines = lines[1:]
        for _ in range(no_intersections):
            intersection_id = int(lines[0][0])
            no_streets = int(lines[1][0])
            lines = lines[2:]
            schedule.schedule[intersection_id] = [
                (name, int(duration)) for name, duration in lines[:no_streets]]
            lines = lines[no_streets:]

        return schedule

    def evaluate(self, city: City):
        # setup green_lights
        street_queue = {city_id: [] for city_id in range(city.no_streets)}
        green_lights = {}
        for intersection_id in self.schedule:
            green_lights[intersection_id] = [
                name for name, time in self.schedule[intersection_id] for _ in range(time)]

        # setup car positions
        car_path = {}
        car_position = {}
        for car in city.cars:
            car_path[car.id] = car.path.copy()
            street_queue[car_path[car.id][0].id].append(car.id)
            car_position[car.id] = car_path[car.id][0].length

        # run simulation
        score = 0
        car_ids = [car.id for car in city.cars]
        for current_time in range(city.duration+1):
            crossed_intersections = []
            for car_id in car_ids:
                if car_path[car_id] == []:
                    continue
                street = car_path[car_id][0]
                if car_position[car_id] < street.length:
                    car_position[car_id] += 1
                    if car_position[car_id] == street.length:
                        if car_path[car_id][1:] == []:
                            score += city.car_value + city.duration - current_time
                            car_path[car_id] = []
                            continue
                        street_queue[street.id].append(car_id)
                if car_position[car_id] == street.length and street_queue[street.id][0] == car_id:
                    intersection_id = city.street_intersection[street.name]
                    light_is_green = green_lights[intersection_id][current_time % len(
                        green_lights[intersection_id])] == street.name
                    if not light_is_green or intersection_id in crossed_intersections:
                        continue
                    crossed_intersections.append(intersection_id)
                    street_queue[street.id] = street_queue[street.id][1:]
                    car_position[car_id] = 0
                    car_path[car_id] = car_path[car_id][1:]
        return score

    def __str__(self):
        s = ""
        for intersection_id in self.schedule:
            s += "On intersection " + str(intersection_id) + " the lights are green for " + str(
                len(self.schedule[intersection_id])) + " incoming streets:\n"
            for tup in self.schedule[intersection_id]:
                name, duration = tup
                s += "- " + name + " for " + str(duration) + " seconds\n"
        return s
