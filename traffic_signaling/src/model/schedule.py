import copy
from .city import City
from queue import Queue


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
            for _ in range(no_streets):
                name, duration = lines[0]
                if intersection_id in schedule.schedule:
                    schedule.schedule[intersection_id].append(
                        (name, int(duration)))
                else:
                    schedule.schedule[intersection_id] = [
                        (name, int(duration))]
                lines = lines[1:]

        return schedule

    def evaluate(self, city: City):
        # street end queues
        street_queue = {}
        for street in city.streets:
            street_queue[street.name] = []

        # current car positions
        car_position = {}
        for car_id in city.cars:
            if city.cars[car_id].path == []:
                raise "Car must start somewhere"
            car = city.cars[car_id]
            car_position[car_id] = (car.path[0].name, car.path[0].length)
            street_queue[car.path[0].name].append(car_id)

        # current intersection green light
        intersection_green_light = {}
        for intersection_id in self.schedule:
            intersection_green_light[intersection_id] = {
                self.schedule[intersection_id][0][0]}
            self.schedule[intersection_id].append(
                self.schedule[intersection_id][0])  # for wrapping

        # copy car paths
        car_paths = {}
        for car_id in city.cars:
            car_paths[car_id] = copy.deepcopy(city.cars[car_id].path)
            car_paths[car_id] = list(map(lambda s: s.name, car_paths[car_id]))

        # run simulation
        score = 0
        remaining = city.duration
        while remaining > 0:
            # update car state
            for car_id in city.cars:
                if car_paths[car_id] == []:
                    score += 1
                name, position = car_position[car_id]
                # car driving on street
                street_length = city.street_length(name)
                if position < street_length:
                    position = position + 1
                    if position == street_length:
                        street_queue[name].append(car_id)
                    car_position[car_id] = (name, position)
                else:
                    if len(car_paths[car_id]) == 1:  # reached destination
                        score += city.bonus
                        car_paths[car_id] = []
                        continue
                    destination = car_paths[car_id][1]
                    for i in intersection_green_light:
                        if intersection_green_light[i] == destination:
                            if street_queue[name] == []:
                                raise "Street queue is empty while car is waiting"
                            if street_queue[name][0] != car_id:
                                continue
                            street_queue[name] = street_queue[name][1:]
                            car_paths[car_id] = car_paths[car_id][1:]
                            car_position[car_id] = (
                                destination, 0)

            # update traffic light state
            for intersection_id in self.schedule:
                name, duration = self.schedule[intersection_id][0]
                if duration == 0:
                    self.schedule[intersection_id].append((name, duration))
                    self.schedule[intersection_id] = self.schedule[intersection_id][1:]
                    intersection_green_light[intersection_id] = self.schedule[intersection_id][0]
                else:
                    duration = duration - 1
                    self.schedule[intersection_id][0] = (name, duration)

            remaining -= 1
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
