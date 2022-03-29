from src.model.city import City
from src.model.schedule import Schedule

example_city = City.from_input('traffic_signaling/asset/ain.txt')


def test_example_solution():
    schedule = Schedule.from_input('traffic_signaling/asset/aout1.txt')
    assert(schedule.evaluate(example_city) == 1002)
