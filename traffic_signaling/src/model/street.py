from queue import Queue


class Street:
    def __init__(self, name: str, length: int):
        self.name = name
        self.length = length

    def __eq__(self, other) -> bool:
        return isinstance(other, Street) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
