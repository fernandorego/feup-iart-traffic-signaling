import time
from model.city import City
from model.schedule import Schedule

if __name__ == '__main__':
    city = City.from_input('traffic_signaling/asset/data/c.txt')
    print("read city")
    schedule = Schedule.from_input('traffic_signaling/asset/out/c1.txt')
    print("read schedule")
    t1 = time.time()
    print(schedule.evaluate(city))
    t2 = time.time()
    print(f'Simulation time: {t2-t1}')
