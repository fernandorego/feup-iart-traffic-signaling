from copy import deepcopy
from math import log, exp
from random import random
from model.city import City
from .common import (
    generate_random_solution,
    distributed_random_sum_permutation,
)
import numpy as np
from matplotlib import pyplot as plt

PATH = "traffic_signaling/asset/out/sa_result.csv"


def simulated_annealing(city: City, iteration_mutation_pairs: list, file_output: bool = True):
    file = None
    if file_output:
        file = open(PATH, "w")
        file.write("INSTANT,SCORE,PROBABILITY,DIFF\n")
        file.flush()

    t = 0
    current_schedule = generate_random_solution(
        city, distributed_random_sum_permutation
    )
    current_schedule.evaluate(city)

    for number_of_iterations, mutation_operator in iteration_mutation_pairs:
        for _ in range(number_of_iterations):
            print(
                f"For t = {t}, simulated annealing reached a score of {current_schedule.last_score}"
            )
            T = scheduling_function(t)
            if T <= 0:
                break
            next_schedule = mutation_operator(deepcopy(current_schedule))
            next_schedule.evaluate(city)

            score_diff = next_schedule.last_score - current_schedule.last_score
            probability = min(exp(score_diff / T), 1)

            print(
                f"Current T = {T}, Probability = {probability}, Score_diff = {score_diff}"
            )
            if file_output:
                file.write(
                    f"{t},{current_schedule.last_score},{probability},{score_diff}\n")
                file.flush()

            if score_diff > 0 or random() < probability:
                current_schedule = next_schedule
            t += 1

    return current_schedule


def scheduling_function(t: float, T0=3000):
    return T0 / (1 + log(1 + t))


def print_sa_results_graph_from_file():
    with open(PATH) as f:
        metrics = [list(map(lambda i: i.strip('\n'), x.split(',')))
                   for x in f.readlines()[1:]]

    xs = np.array([int(x[0]) for x in metrics])
    scores = np.array([int(x[1]) for x in metrics])
    plt.plot(xs, scores)

    plt.title('Simulated annealing')

    plt.xlabel("Iteration")
    plt.ylabel("Solution score")
    plt.show()
