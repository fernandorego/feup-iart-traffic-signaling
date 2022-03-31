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
        # street queues
        street_queue = {}
        for s in city.streets:
            street_queue[s.name] = []

        # car positions
        car_path = {}
        car_position = {}
        for car in city.cars:
            car_path[car.id] = [s.name for s in car.path]
            street_queue[car_path[car.id][0]].append(
                car.id)
            car_position[car.id] = city.street_length(car_path[car.id][0])

        # setup green_lights
        green_lights = {}
        for intersection_id in self.schedule:
            green_lights[intersection_id] = []
            for name, time in self.schedule[intersection_id]:
                green_lights[intersection_id].extend(
                    [name for _ in range(time)])

        score = 0
        car_ids = [car.id for car in city.cars]
        for current_time in range(city.duration+1):
            for car_id in car_ids:
                if car_path[car_id] == []:
                    continue
                street_name = car_path[car_id][0]
                street_length = city.street_length(street_name)
                if car_position[car_id] < street_length:
                    car_position[car_id] += 1
                    if car_position[car_id] == street_length:
                        if car_path[car_id][1:] == []:
                            score += city.bonus + city.duration - current_time
                            car_path[car_id] = []
                            break
                        street_queue[street_name].append(car_id)
                if car_position[car_id] == street_length and street_queue[street_name][0] == car_id:
                    for intersection_id in self.schedule:
                        if green_lights[intersection_id][current_time % len(green_lights[intersection_id])] != street_name:
                            continue
                        street_queue[street_name] = street_queue[street_name][1:]
                        car_position[car_id] = 0
                        car_path[car_id] = car_path[car_id][1:]
                        break
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
