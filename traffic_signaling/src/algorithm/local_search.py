from random import randint, random
from algorithm.common import distributed_sum_permutation, generate_random_solution, mutate_intersection, mutate_schedule, random_sum_permutation
from model.city import City
from model.schedule import Schedule


def iterated_local_search(city: City, number_of_iterations: int, number_of_mutations_per_iteration: int):
    first_solution = generate_random_solution(
        city, distributed_sum_permutation)
    current_max = first_solution, first_solution.evaluate(city)
    for i in range(number_of_iterations):
        perturbation = mutate_schedule(
            city, current_max[0], 0.0001*(number_of_iterations-i)/number_of_iterations)
        current = perturbation, perturbation.evaluate(city)
        mutations = []
        for _ in range(number_of_mutations_per_iteration):
            candidate, _ = mutate_intersection(city, current[0])
            mutations.append((candidate, candidate.evaluate(city)))
        best_candidate = max(mutations, key=lambda x: x[1])
        if best_candidate[1] > current_max[1]:
            current_max = best_candidate
        print(best_candidate[1], current_max[1])
    return current_max
