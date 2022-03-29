from model.city import City
from model.schedule import Schedule

if __name__ == '__main__':
    city = City.from_input('traffic_signaling/asset/input_sample.txt')
    print(city)
    schedule = Schedule.from_input('traffic_signaling/asset/output_sample.txt')
    print(schedule)
