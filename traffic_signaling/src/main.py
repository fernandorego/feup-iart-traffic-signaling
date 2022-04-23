from random import seed
from model.city import City
from model.schedule import Schedule
from algorithm.common import (
    generate_random_solution,
    mutate_intersection,
    mutate_schedule,
    mutate_single_street,
)
from algorithm.annealing import print_sa_results_graph_from_file, simulated_annealing
from algorithm.genetics import genetic_algorithm, print_genetic_results_graph_from_file
from algorithm.local_search import iterated_local_search, print_ils_results_graph_from_file
from algorithm.taboo import print_taboo_results_graph_from_file, taboo_search

if __name__ == "__main__":
    seed()
    city = City.from_input("traffic_signaling/asset/data/e.txt")
    #taboo_search(city, 12, 1)
    # print_taboo_results_graph_from_file()
    #iterated_local_search(city, 100, 10)
    # print_ils_results_graph_from_file()
    genetic_algorithm(city, 20, 10, 5, 0.2)
    print_genetic_results_graph_from_file()
    # iteration_mutation_pairs = [(100, lambda x: mutate_schedule(city, x, 0.5)), (
    # 10, lambda x: mutate_intersection(city, x)[0]), (10, lambda x: mutate_single_street(city, x))]
    #schedule = simulated_annealing(city, iteration_mutation_pairs)
    # print_sa_results_graph_from_file()
    # print("read city")
    # schedule = Schedule.from_input('traffic_signaling/asset/out/d1.txt')
    # print("read schedule")
    # t1 = time.time()
    # print(schedule.evaluate(city))
    # t2 = time.time()
    # print(f'Simulation time: {t2-t1}')
