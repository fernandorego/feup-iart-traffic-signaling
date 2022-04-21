from random import seed
from model.city import City
from model.schedule import Schedule
from algorithm.common import generate_random_solution, mutate_intersection, mutate_schedule, mutate_single_street, random_sum_permutation
from algorithm.annealing import simulated_annealing
from algorithm.local_search import iterated_local_search
from algorithm.taboo import taboo_search

if __name__ == "__main__":
    seed()
    city = City.from_input("traffic_signaling/asset/data/e.txt")
    # genetic_algorithm(city, 50, 200, 40, 0.05)
    schedule = simulated_annealing(city, 100, lambda x: mutate_schedule(city, x, 0.1))
    schedule = simulated_annealing(city, 100, lambda x: mutate_intersection(city, x)[0], schedule)
    schedule = simulated_annealing(city, 100, lambda x: mutate_single_street(city, x), schedule)
    # print("read city")
    # schedule = Schedule.from_input('traffic_signaling/asset/out/d1.txt')
    # print("read schedule")
    # t1 = time.time()
    # print(schedule.evaluate(city))
    # t2 = time.time()
    # print(f'Simulation time: {t2-t1}')
