from model.city import City
from model.schedule import Schedule

if __name__ == '__main__':
    city = City.from_input('traffic_signaling/asset/data/b.txt')
    schedule = Schedule.from_input('traffic_signaling/asset/out/b1.txt')
    print(schedule.evaluate(city))
