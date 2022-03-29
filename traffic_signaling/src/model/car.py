class Car:
    def __init__(self, path: list):
        self.path = path

    def __eq__(self, other):
        return isinstance(other, Car) and other.path == self.path
