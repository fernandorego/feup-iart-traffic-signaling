from traffic_signaling.src.model.city import City
from traffic_signaling.src.model.schedule import Schedule

a_city = City.from_input('traffic_signaling/asset/data/a.txt')
b_city = City.from_input('traffic_signaling/asset/data/b.txt')
c_city = City.from_input('traffic_signaling/asset/data/c.txt')
d_city = City.from_input('traffic_signaling/asset/data/d.txt')
e_city = City.from_input('traffic_signaling/asset/data/e.txt')
f_city = City.from_input('traffic_signaling/asset/data/f.txt')


def test_a_solution1():
    schedule = Schedule.from_input('traffic_signaling/asset/out/a1.txt')
    assert(schedule.evaluate(a_city) == 1002)


def test_a_solution2():
    schedule = Schedule.from_input('traffic_signaling/asset/out/a2.txt')
    assert(schedule.evaluate(a_city) == 1001)


def test_a_solution3():
    schedule = Schedule.from_input('traffic_signaling/asset/out/a3.txt')
    assert(schedule.evaluate(a_city) == 2002)


def test_e_solution1():
    schedule = Schedule.from_input('traffic_signaling/asset/out/e1.txt')
    assert(schedule.evaluate(e_city) == 681875)


def test_e_solution2():
    schedule = Schedule.from_input('traffic_signaling/asset/out/e2.txt')
    assert(schedule.evaluate(e_city) == 710095)


def test_b_solution1():
    schedule = Schedule.from_input('traffic_signaling/asset/out/b1.txt')
    assert(schedule.evaluate(b_city) == 4566783)


def test_f_solution1():
    schedule = Schedule.from_input('traffic_signaling/asset/out/f1.txt')
    assert(schedule.evaluate(f_city) == 1408553)


def test_c_solution1():
    schedule = Schedule.from_input('traffic_signaling/asset/out/c1.txt')
    assert(schedule.evaluate(c_city) == 1299593)


def test_d_solution1():
    schedule = Schedule.from_input('traffic_signaling/asset/out/d1.txt')
    assert(schedule.evaluate(d_city) == 1586428)
