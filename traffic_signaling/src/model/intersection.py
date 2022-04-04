class Intersection:
    def __init__(self):
        self.id = id
        self.incoming_streets = set()
        self.outgoing_streets = set()
        self.x, self.y = -1, -1

    def __str__(self):
        return str(self.id)

    def get_pos(self) -> tuple:
        return (self.x, self.y)

    def set_pos(self, x, y) -> None:
        self.x = x
        self.y = y
