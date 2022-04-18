from random import random, seed
import time
from model.city import City
from algorithm.local_search import iterated_local_search
from algorithm.taboo import taboo_search

if __name__ == "__main__":
    seed()
    city = City.from_input("traffic_signaling/asset/data/e.txt")
    schedule = iterated_local_search(city, 100, 2)
    schedule[0].write_to_file(".", "my_solution")
    #genetic_algorithm(city, 50, 150, 30, 0.05)
    # print("read city")
    # schedule = Schedule.from_input('traffic_signaling/asset/out/d1.txt')
    # print("read schedule")
    # t1 = time.time()
    # print(schedule.evaluate(city))
    # t2 = time.time()
    # print(f'Simulation time: {t2-t1}')
