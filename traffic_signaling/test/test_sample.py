from traffic_signaling.src.model.city import City
from traffic_signaling.src.model.schedule import Schedule

example_city = City.from_input('traffic_signaling/asset/ain.txt')


def test_example_solution1():
    schedule = Schedule.from_input('traffic_signaling/asset/aout1.txt')
    assert(schedule.evaluate(example_city) == 1002)


def test_example_solution2():
    schedule = Schedule.from_input('traffic_signaling/asset/aout2.txt')
    assert(schedule.evaluate(example_city) == 2002)
