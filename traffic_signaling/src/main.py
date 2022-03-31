from model.city import City
from model.schedule import Schedule

if __name__ == '__main__':
    city = City.from_input('traffic_signaling/asset/data/a.txt')
    schedule = Schedule.from_input('traffic_signaling/asset/out/a1.txt')
    # print(schedule)
    print(schedule.evaluate(city))

    schedule1 = Schedule.from_input('traffic_signaling/asset/out/a3.txt')
    # print(schedule1)
    print(schedule1.evaluate(city))
