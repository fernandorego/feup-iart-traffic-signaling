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

        # copy schedule
        schedule = copy.deepcopy(self.schedule)

        # current intersection green light
        intersection_green_light = {}
        for intersection_id in schedule:
            intersection_green_light[intersection_id] = schedule[intersection_id][0][0]

        # copy car paths
        car_paths = {}
        for car_id in city.cars:
            car_paths[car_id] = copy.deepcopy(city.cars[car_id].path)
            car_paths[car_id] = [s.name for s in car_paths[car_id]]

        # run simulation
        score = 0
        remaining = city.duration
        while 1:
            # update car state
            for car_id in city.cars:
                if len(car_paths[car_id]) == 0:  # is parked at the final street
                    score += 1
                    continue
                name, position = car_position[car_id]
                street_length = city.street_length(name)
                # car driving on street
                if position < street_length:
                    position += 1
                    car_position[car_id] = (name, position)
                    if position == street_length:
                        street_queue[name].append(car_id)
                else:
                    destination = car_paths[car_id][1]
                    for i in intersection_green_light:
                        if intersection_green_light[i] == destination:
                            if street_queue[name][0] != car_id:
                                continue
                            street_queue[name] = street_queue[name][1:]
                            car_paths[car_id] = car_paths[car_id][1:]
                            print(car_id, str(
                                car_paths[car_id]), car_position[car_id], remaining)
                            car_position[car_id] = (destination, 0)
                            break
                    if len(car_paths[car_id]) == 1:  # reached final destination
                        score += city.bonus
                        car_paths[car_id] = []
                        continue

            # no time left
            if remaining == 0:
                return score
            remaining -= 1

            # update traffic light state
            for intersection_id in schedule:
                name, duration = schedule[intersection_id][0]
                duration = duration - 1
                if duration <= 0:
                    schedule[intersection_id].append(
                        (name, [i[1] for i in self.schedule[intersection_id] if i[0] == name][0]))
                    schedule[intersection_id] = schedule[intersection_id][1:]
                    intersection_green_light[intersection_id] = schedule[intersection_id][0][0]
                else:
                    schedule[intersection_id][0] = (name, duration)

    def __str__(self):
        s = ""
        for intersection_id in self.schedule:
            s += "On intersection " + str(intersection_id) + " the lights are green for " + str(
                len(self.schedule[intersection_id])) + " incoming streets:\n"
            for tup in self.schedule[intersection_id]:
                name, duration = tup
                s += "- " + name + " for " + str(duration) + " seconds\n"
        return s
