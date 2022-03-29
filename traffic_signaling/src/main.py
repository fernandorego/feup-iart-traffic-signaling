from model.city import City
from model.schedule import Schedule

if __name__ == '__main__':
    city = City.from_input('traffic_signaling/asset/ain.txt')
    print(city)

    schedule = Schedule.from_input('traffic_signaling/asset/aout1.txt')
    print(schedule)
    print()
    print(schedule.evaluate(city))
    print()

    schedule1 = Schedule.from_input('traffic_signaling/asset/aout2.txt')
    print(schedule1)
    print()
    print(schedule1.evaluate(city))
    print()
