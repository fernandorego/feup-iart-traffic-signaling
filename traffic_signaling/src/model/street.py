from queue import Queue
from tracemalloc import start


class Street:
    def __init__(self, name: str, length: int, start_intersection: int, end_intersection: int, traffic_light_green: bool):
        self.name = name
        self.length = length
        self.end_queue = Queue()
        self.running_cars = [None for _ in range(length-1)]
        self.start_intersection = start_intersection
        self.end_intersection = end_intersection
        self.traffic_light_green = traffic_light_green

    def __eq__(self, other) -> bool:
        return isinstance(other, Street) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        s = "Street " + self.name + " starts at intersection " + \
            str(self.start_intersection) + ", ends at " + \
            str(self.end_intersection) + " and has L=" + \
            str(self.length) + "\nCars on street: " + str(self.running_cars) + \
            "; Cars waiting on the end: " + \
            str([c.id for c in list(self.end_queue.queue)]) + "; Traffic light: " + \
            ("GREEN" if self.traffic_light_green else "RED") + "\n"
        return s
