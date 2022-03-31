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

        # copy schedule
        next_lights = copy.deepcopy(self.schedule)

        score = 0
        car_ids = [car.id for car in city.cars]
        for _ in range(city.duration+1):
            # update car positions
            for car_id in car_ids:
                if car_path[car_id] == []:
                    score += 1
                    continue
                street_name = car_path[car_id][0]
                street_length = city.street_length(street_name)
                if car_position[car_id] < street_length:
                    car_position[car_id] += 1
                    if car_position[car_id] == street_length:
                        if car_path[car_id][1:] == []:
                            score += city.bonus
                            car_path[car_id] = []
                            break
                        street_queue[street_name].append(car_id)
                if car_position[car_id] == street_length and street_queue[street_name][0] == car_id:
                    for intersection_id in self.schedule:
                        if next_lights[intersection_id][0][0] != street_name:
                            continue
                        street_queue[street_name] = street_queue[street_name][1:]
                        car_position[car_id] = 0
                        car_path[car_id] = car_path[car_id][1:]
                        break

            # update intersection lights
            for intersection_id in self.schedule:
                incoming_street_name, duration = next_lights[intersection_id][0]
                duration -= 1
                if duration == 0:
                    next_lights[intersection_id] = next_lights[intersection_id][1:]
                    if next_lights[intersection_id] == []:
                        next_lights[intersection_id] = self.schedule[intersection_id].copy(
                        )
                else:
                    next_lights[intersection_id][0] = (
                        incoming_street_name, duration)
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
