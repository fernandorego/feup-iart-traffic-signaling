from random import randint, random
from algorithm.common import (
    distributed_sum_permutation,
    generate_random_solution,
    mutate_intersection,
    mutate_schedule,
    distributed_random_sum_permutation,
)
from model.city import City
from model.schedule import Schedule


def iterated_local_search(
    city: City,
    number_of_iterations: int,
    number_of_mutations_per_iteration: int,
    perturbation_factor: int = 1,
    file_output: bool = True
):
    file = None
    if file_output:
        file = open("traffic_signaling/asset/out/ils_result.csv", "w")
        file.write("ITERATION,PERTURBATION_STRENGTH,TENTATIVE_SCORE,BEST_SCORE\n")
        file.flush()

    first_solution = generate_random_solution(
        city, distributed_random_sum_permutation)
    current_max = first_solution, first_solution.evaluate(city)
    for i in range(number_of_iterations):
        perturbation_strength = perturbation_factor * \
            (number_of_iterations - i) / number_of_iterations
        perturbation = mutate_schedule(
            city,
            current_max[0],
            perturbation_strength
        )
        current = perturbation, perturbation.evaluate(city)
        mutations = []
        for _ in range(number_of_mutations_per_iteration):
            candidate, _ = mutate_intersection(city, current[0])
            mutations.append((candidate, candidate.evaluate(city)))
        best_candidate = max(mutations, key=lambda x: x[1])
        if best_candidate[1] > current_max[1]:
            current_max = best_candidate
        print(
            f"On iteration {i}, iterated local search found a score of {best_candidate[1]}. Best score yet is {current_max[1]}")
        if file_output:
            file.write(
                f"{i},{perturbation_strength},{best_candidate[1]},{current_max[1]}\n")
            file.flush()
    return current_max
