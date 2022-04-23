from random import seed
from model.city import City
from model.schedule import Schedule
from algorithm.common import (
    generate_random_solution,
    mutate_intersection,
    mutate_schedule,
    mutate_single_street,
)
from algorithm.annealing import simulated_annealing
from algorithm.genetics import genetic_algorithm
from algorithm.local_search import iterated_local_search
from algorithm.taboo import taboo_search

if __name__ == "__main__":
    seed()
    city = City.from_input("traffic_signaling/asset/data/e.txt")
    taboo_search(city, 50, 2)
    #iterated_local_search(city, 100, 10)
    #genetic_algorithm(city, 50, 100, 20, 0.1)
    # iteration_mutation_pairs = [(100, lambda x: mutate_schedule(city, x, 0.1)), (
    # 100, lambda x: mutate_intersection(city, x)[0]), (100, lambda x: mutate_single_street(city, x))]
    #schedule = simulated_annealing(city, iteration_mutation_pairs)
    # print("read city")
    # schedule = Schedule.from_input('traffic_signaling/asset/out/d1.txt')
    # print("read schedule")
    # t1 = time.time()
    # print(schedule.evaluate(city))
    # t2 = time.time()
    # print(f'Simulation time: {t2-t1}')
