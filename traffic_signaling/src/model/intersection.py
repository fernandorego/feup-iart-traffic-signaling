class Intersection:
    def __init__(self, id):
        self.id = id
        self.incoming_streets = set()
        self.outgoing_streets = set()
        self.x, self.y = -1, -1

    def __str__(self):
        return str(self.id)

    def get_pos(self) -> tuple:
        """
        Get intersection position

        Return:
            tuple with intersection coordinates
        """
        return (self.x, self.y)

    def set_pos(self, x, y) -> None:
        '''Set intersection coordinates'''
        self.x = x
        self.y = y
