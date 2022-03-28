from .car import Car
from .street import Street


class City:
    def __init__(self, cars: set, streets: set, remaining_seconds: int, bonus: int):
        self.cars = cars
        self.streets = streets
        self.remaining_seconds = remaining_seconds
        self.bonus = bonus
        self.score = 0

    def __init__(self):
        self.cars = set()
        self.streets = set()
        self.remaining_seconds = 0
        self.bonus = 0
        self.score = 0

    def from_input(input_file: str):
        with open(input_file) as f:
            lines = f.readlines()
        city = City()
        duration, _, no_streets, no_cars, bonus = lines[0].split(
            ' ')
        city.bonus = int(bonus)
        city.remaining_seconds = int(duration)
        for line in lines[1:1+int(no_streets)]:
            line = line.strip('\n').split(' ')
            street = Street(line[2], int(line[3]), int(
                line[0]), int(line[1]), False)
            city.streets.add(street)
        current_car: int = 0
        for line in lines[1+int(no_streets):1+int(no_streets)+int(no_cars)]:
            line = line.strip('\n').split(' ')
            path = []
            for name in line[1:]:
                for s in city.streets:
                    if s.name == name:
                        path.append(s)
            car = Car(current_car, path[1:])
            path[0].end_queue.put(car)
            city.cars.add(car)
            current_car += 1
        return city

    def __str__(self):
        s = ""
        s += "Remaining seconds: " + str(self.remaining_seconds) + "\n"
        s += "Current score: " + str(self.score) + "\n"
        s += "--------\n"
        for street in self.streets:
            s += str(street) + "\n"
        s += "--------\n"
        for car in self.cars:
            s += "Car " + str(car.id) + " follows path: ["
            for street in car.path:
                s += street.name + ", "
            s = s[:len(s)-2]
            s += "]\n"
        return s
