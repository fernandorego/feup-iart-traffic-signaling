class Car:
    def __init__(self, id: int, path: list):
        self.id = id
        self.path = path

    def __eq__(self, other):
        return isinstance(other, Car) and other.path == self.path

    def __hash__(self) -> int:
        return hash(self.id)
