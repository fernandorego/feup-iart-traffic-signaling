from .car import Car
from .street import Street
from .intersection import Intersection


class City:
    def __init__(self):
        self.cars = []
        self.streets = set()
        self.intersections = dict()
        self.duration = 0
        self.bonus = 0

    def from_input(input_file: str):
        with open(input_file) as f:
            lines = f.readlines()
        lines = [line.strip('\n').split(' ') for line in lines]

        city = City()
        duration, _, no_streets, no_cars, bonus = lines[0]
        city.bonus = int(bonus)
        city.duration = int(duration)

        # add streets
        for line in lines[1:1+int(no_streets)]:
            start_intersection_id = int(line[0])
            end_intersection_id = int(line[1])
            street = Street(line[2], int(line[3]))
            city.streets.add(street)

            # add start intersection
            if start_intersection_id in city.intersections:
                city.intersections[start_intersection_id].outgoing_streets.add(
                    street)
            else:
                start_intersection = Intersection()
                start_intersection.outgoing_streets.add(street)
                city.intersections[start_intersection_id] = start_intersection

            # add end intersection
            if end_intersection_id in city.intersections:
                city.intersections[end_intersection_id].incoming_streets.add(
                    street)
            else:
                end_intersection = Intersection()
                end_intersection.incoming_streets.add(street)
                city.intersections[end_intersection_id] = end_intersection

        # add cars
        current_car: int = 0
        for line in lines[1+int(no_streets):1+int(no_streets)+int(no_cars)]:
            path = []
            for name in line[1:]:
                path.append([s for s in city.streets if s.name == name][0])
            car = Car(current_car, path)
            city.cars.append(car)
            current_car += 1
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

    def street_length(self, name: str):
        for s in self.streets:
            if s.name == name:
                return s.length
        raise Exception("Street not found")
