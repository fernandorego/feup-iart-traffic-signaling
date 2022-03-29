class TrafficLight:
    RED = 0
    GREEN = 1


class Intersection:
    def __init__(self, id: int):
        self.id = id
        self.incoming_streets = dict()
        self.outgoing_streets = set()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Intersection) and self.id == other.id

    def __hash__(self):
        return self.id

    def __str__(self):
        return str(self.id)
