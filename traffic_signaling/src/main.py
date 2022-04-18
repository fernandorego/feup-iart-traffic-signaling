from random import random, seed
import time
from model.city import City
from algorithm.taboo import taboo_search
from algorithm.local_search import iterated_local_search

if __name__ == "__main__":
    seed()
    city = City.from_input("traffic_signaling/asset/data/e.txt")
    print(iterated_local_search(city, 50, 5))
    #genetic_algorithm(city, 50, 150, 30, 0.05)
    # print("read city")
    # schedule = Schedule.from_input('traffic_signaling/asset/out/d1.txt')
    # print("read schedule")
    # t1 = time.time()
    # print(schedule.evaluate(city))
    # t2 = time.time()
    # print(f'Simulation time: {t2-t1}')
