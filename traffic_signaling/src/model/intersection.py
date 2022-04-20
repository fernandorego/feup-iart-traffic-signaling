class Intersection:
    def __init__(self, id):
        self.id = id
        self.incoming_streets = set()
        self.outgoing_streets = set()

    def __str__(self):
        return str(self.id)
