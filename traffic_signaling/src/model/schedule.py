class Schedule:
    def __init__(self):
        self.schedule = dict()

    def from_input(input_file: str):
        with open(input_file) as f:
            lines = f.readlines()
        lines = [line.strip('\n').split(' ') for line in lines]

        schedule = Schedule()
        no_intersections = int(lines[0][0])
        lines = lines[1:]
        for _ in range(no_intersections):
            intersection_id = int(lines[0][0])
            no_streets = int(lines[1][0])
            lines = lines[2:]
            for _ in range(no_streets):
                name, duration = lines[0]
                if intersection_id in schedule.schedule:
                    schedule.schedule[intersection_id].append(
                        (name, duration))
                else:
                    schedule.schedule[intersection_id] = [(name, duration)]
                lines = lines[1:]

        return schedule

    def __str__(self):
        s = ""
        for intersection_id in self.schedule:
            s += "On intersection " + str(intersection_id) + " the lights are green for " + str(
                len(self.schedule[intersection_id])) + " incoming streets:\n"
            for tup in self.schedule[intersection_id]:
                name, duration = tup
                s += "- " + name + " for " + str(duration) + " seconds\n"
        return s
