from controller.main_controller import MainController
from controller.pygame_controller import PygameController
from model.city import City
from model.schedule import Schedule

# if __name__ == '__main__':

#city = City.from_input('../asset/data/a.txt')
#schedule = Schedule.from_input('../asset/out/a1.txt')
#controller = PygameController(city)
# controller.simulate(schedule)

#t1 = time.time()
# print(schedule.evaluate(city))
#t2 = time.time()
#print(f'Simulation time: {t2-t1}')


if __name__ == "__main__":
    #city = City.from_input('traffic_signaling/asset/data/e.txt')
    #schedule = Schedule.from_input('traffic_signaling/asset/out/e1.txt')
    #controller = PygameController(city)
    # controller.simulate(schedule)
    main_controller = MainController()
    main_controller.main_loop()
