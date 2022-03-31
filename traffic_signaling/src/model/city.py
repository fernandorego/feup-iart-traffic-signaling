from .car import Car
from .street import Street
from .intersection import Intersection


class City:
    def __init__(self):
        self.cars = []
        self.streets = []
        self.intersections = {}  # by intersection_id
        self.street_intersection = {}  # by street name
        self.no_streets = 0
        self.duration = 0
        self.car_value = 0

    def from_input(input_file: str):
        with open(input_file) as f:
            lines = f.readlines()
        lines = [line.strip('\n').split(' ') for line in lines]

        city = City()
        duration, no_intersections, no_streets, no_cars, bonus = lines[0]
        city.no_streets = int(no_streets)
        city.car_value = int(bonus)
        city.duration = int(duration)

        # add blank intersections
        for intersection_id in range(int(no_intersections)):
            city.intersections[intersection_id] = Intersection()

        # connect intersections through streets
        street_by_name = {}  # helper for later exploring cars
        city_id = 0
        for line in lines[1:1+int(no_streets)]:
            start_intersection_id = int(line[0])
            end_intersection_id = int(line[1])
            street = Street(city_id, line[2], int(line[3]))
            street_by_name[street.name] = street
            city.streets.append(street)
            city.intersections[start_intersection_id].outgoing_streets.add(
                street)
            city.intersections[end_intersection_id].incoming_streets.add(
                street)
            city_id += 1

        # add cars
        current_car: int = 0
        for line in lines[1+int(no_streets):1+int(no_streets)+int(no_cars)]:
            path = [street_by_name[name] for name in line[1:]]
            car = Car(current_car, path)
            city.cars.append(car)
            current_car += 1

        # calculate helper street intersection
        for intersection_id in city.intersections:
            for incoming_street in city.intersections[intersection_id].incoming_streets:
                city.street_intersection[incoming_street.name] = intersection_id

        return city

    def __str__(self):
        s = ""
        s += "Duration: " + str(self.duration) + "\n"
        s += "--------\n"
        for street in self.streets:
            s += str(street.name) + " has L=" + str(street.length) + "\n"
        s += "--------\n"
        for car in self.cars:
            s += "Car " + str(car.id) + " path: " + \
                str([st.name for st in car.path]) + "\n"
        s += "--------\n"
        for intersection_id in self.intersections:
            s += "Intersection " + str(intersection_id) + " connects " + str(
                [st.name for st in self.intersections[intersection_id].incoming_streets]) + " to "\
                + str([st.name for st in self.intersections[intersection_id].outgoing_streets]) + "\n"
        return s
