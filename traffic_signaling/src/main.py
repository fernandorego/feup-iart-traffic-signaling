import time
from model.city import City
from model.schedule import Schedule
from controller.city_controller import CityController
from controller.pygame_controller import PygameController

if __name__ == '__main__':

    city = City.from_input('../asset/data/a.txt')
    schedule = Schedule.from_input('../asset/out/a1.txt')
    controller = PygameController(city)
    controller.simulate(schedule)

    #t1 = time.time()
    # print(schedule.evaluate(city))
    #t2 = time.time()
    #print(f'Simulation time: {t2-t1}')
