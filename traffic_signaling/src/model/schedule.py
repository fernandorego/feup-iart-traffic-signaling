from time import sleep
from .city import City


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
                name for name, duration in lines[:no_streets] for _ in range(int(duration))]
            lines = lines[no_streets:]

        return schedule

    def evaluate(self, city: City):
        # setup simulation helpers
        street_queue = {city_id: [] for city_id in range(city.no_streets)}
        car_path = {}
        next_analysed_time = {}
        for car in city.cars:
            car_path[car.id] = car.path
            street_queue[car_path[car.id][0].id].append(car.id)
            next_analysed_time[car.id] = 0

        # run simulation
        score = 0
        for current_time in range(city.duration+1):
            crossed_intersections = []
            scheduled_removals = []
            for car_id in car_path:
                if next_analysed_time[car_id] > current_time:
                    continue
                street = car_path[car_id][0]
                if street_queue[street.id][0] != car_id:
                    continue
                intersection_id = city.street_intersection[street.name]
                light_is_green = self.schedule[intersection_id][current_time %
                                                                len(self.schedule[intersection_id])] == street.name
                if not light_is_green or intersection_id in crossed_intersections:
                    continue
                crossed_intersections.append(intersection_id)
                street_queue[street.id] = street_queue[street.id][1:]
                car_path[car_id] = car_path[car_id][1:]
                next_street = car_path[car_id][0]
                next_time = current_time + next_street.length
                if car_path[car_id][1:] == []:
                    scheduled_removals.append(car_id)
                    if next_time > city.duration:
                        continue
                    score += city.car_value + city.duration - next_time
                else:
                    street_queue[next_street.id].append(car_id)
                    next_analysed_time[car_id] = next_time
            for car_id in scheduled_removals:
                del car_path[car_id]
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
