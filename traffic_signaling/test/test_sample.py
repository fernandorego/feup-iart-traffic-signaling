from traffic_signaling.src.model.city import City
from traffic_signaling.src.model.schedule import Schedule

a_city = City.from_input('traffic_signaling/asset/data/a.txt')
b_city = City.from_input('traffic_signaling/asset/data/b.txt')


def test_example_solution1():
    schedule = Schedule.from_input('traffic_signaling/asset/out/a1.txt')
    assert(schedule.evaluate(a_city) == 1002)


def test_example_solution2():
    schedule = Schedule.from_input('traffic_signaling/asset/out/a2.txt')
    assert(schedule.evaluate(a_city) == 2002)


def test_example_solution3():
    schedule = Schedule.from_input('traffic_signaling/asset/out/b1.txt')
    assert(schedule.evaluate(b_city) == 707937)
