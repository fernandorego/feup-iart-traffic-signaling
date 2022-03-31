from model.city import City
from model.schedule import Schedule

if __name__ == '__main__':
    city = City.from_input('traffic_signaling/asset/data/a.txt')
    print(city)
    schedule = Schedule.from_input('traffic_signaling/asset/out/a1.txt')
    # print(schedule)
    print()
    print(schedule.evaluate(city))
    print()

    schedule1 = Schedule.from_input('traffic_signaling/asset/out/a2.txt')
    # print(schedule1)
    print()
    print(schedule1.evaluate(city))
    print()
