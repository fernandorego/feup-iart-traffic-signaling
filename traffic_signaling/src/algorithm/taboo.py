from random import randint
from algorithm.common import distributed_random_sum_permutation, generate_random_solution, mutate_intersection
from model.city import City
import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy

PATH = "traffic_signaling/asset/out/taboo_result.csv"


def taboo_search(city: City, number_of_iterations: int, number_of_mutations_per_iteration: int,
                 max_worse_jump_percentage: int = 0.1, file_output: bool = True, initial_schedule=None):
    """
    For a given initial schedule, performs a taboo search.
    The neighbourhood is given by the mutate_intersection operator, with the mutated intersection being the taboo criterion.
    Resets to the best found global solution if current solution is given percentage worse than the aforementioned.

    Parameters:
        city: problem city
        number_of_iterations: number of iterations until stopping
        number_of_mutations_per_iteration: neighbourhood size to look for
        max_worse_jump_percentage: max distance to global maxima before resetting to it
        file_output: whether to write the results to a file
        initial_schedule: the algorithm initial schedule (random if None)

    Return:
        Final best solution found
    """
    file = None
    if file_output:
        file = open(PATH, "w")
        file.write("ITERATION,TENTATIVE_SCORE,BEST_SCORE\n")
        file.flush()

    first_solution = generate_random_solution(
        city, distributed_random_sum_permutation) if initial_schedule is None else initial_schedule
    current = first_solution, first_solution.evaluate(city)
    avg_score = current[1]
    current_max = current
    taboo_memory = {intersection_no: 0 for intersection_no in range(
        city.no_intersections)}
    improvement_to_max = 0
    for i in range(number_of_iterations):
        mutations = []
        mutated, tries = 0, 0
        while mutated < number_of_mutations_per_iteration:
            candidate, mutated_intersection = mutate_intersection(
                city, deepcopy(current[0]))
            if tries > 100 or taboo_memory[mutated_intersection.id] <= 0:
                mutations.append(
                    (candidate, mutated_intersection, candidate.evaluate(city)))
                mutated += 1
                tries = 0
            tries += 1
        taboo_memory = {intersection_id: max(
            0, taboo_memory[intersection_id]-1) for intersection_id in taboo_memory}
        best_candidate = max(mutations, key=lambda x: x[2])
        current = (best_candidate[0], best_candidate[2])
        taboo_memory[best_candidate[1].id] = randint(
            0, (number_of_iterations - i) // 2)
        improvement_to_max = current[1] - current_max[1]
        if improvement_to_max > 0:
            current_max = tuple(current)

        print(
            f"On iteration {i}, taboo search found a score of {current[1]}. Best score yet is {current_max[1]}")
        if file_output:
            file.write(f"{i},{current[1]},{current_max[1]}\n")
            file.flush()

        if -improvement_to_max > avg_score//(1/max_worse_jump_percentage):
            current = current_max

    return current_max[0]


def print_taboo_results_graph_from_file():
    """
    Show matplot graph in the screen containing the taboo search information
    lastly written in a file in the default location.
    """
    with open(PATH) as f:
        metrics = [list(map(lambda i: i.strip('\n'), x.split(',')))
                   for x in f.readlines()[1:]]

    xs = np.array([int(x[0]) for x in metrics])
    ys = np.array([int(x[1]) for x in metrics])
    plt.plot(xs, ys)

    plt.title('Taboo search')

    plt.xlabel("Iteration")
    plt.ylabel("Solution score")
    plt.show()
