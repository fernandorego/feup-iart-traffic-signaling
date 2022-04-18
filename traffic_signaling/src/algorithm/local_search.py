from random import randint, random
from algorithm.common import distributed_sum_permutation, generate_random_solution, mutate_intersection
from model.city import City
from model.schedule import Schedule


def iterated_local_search(city: City, number_of_iterations: int, number_of_mutations_per_iteration: int):
    first_solution = generate_random_solution(
        city, distributed_sum_permutation)
    current_max = first_solution, first_solution.evaluate(city)
    for i in range(number_of_iterations):
        another_solution = generate_random_solution(
            city, distributed_sum_permutation)
        perturbation = Schedule()
        for j in range(city.no_intersections):
            if random() < (number_of_iterations - i) / number_of_iterations:
                perturbation.schedule[j] = another_solution.schedule[j]
            else:
                perturbation.schedule[j] = current_max[0].schedule[j]
        current = perturbation, perturbation.evaluate(city)
        mutations = []
        for _ in range(number_of_mutations_per_iteration):
            candidate, _ = mutate_intersection(city, current[0])
            mutations.append((candidate, candidate.evaluate(city)))
        best_candidate = max(mutations, key=lambda x: x[1])
        if best_candidate[1] > current_max[1]:
            current_max = best_candidate
        print(best_candidate[1], current_max)
    return current_max
