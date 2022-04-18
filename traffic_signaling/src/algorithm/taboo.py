from random import randint
from traffic_signaling.src.algorithm.common import distributed_sum_permutation, generate_random_solution, mutate_intersection
from traffic_signaling.src.model.city import City
from traffic_signaling.src.model.schedule import Schedule


def taboo_search(city: City, number_of_iterations: int, number_of_mutations_per_iteration: int):
    first_solution = generate_random_solution(
        city, distributed_sum_permutation)
    current = first_solution, first_solution.evaluate(city)
    current_max = current
    taboo_memory = {intersection_no: 0 for intersection_no in range(
        city.no_intersections)}
    for _ in range(number_of_iterations):
        mutations = []
        for _ in range(number_of_mutations_per_iteration):
            candidate, mutated_intersection = mutate_intersection(
                city, current[0])
            if taboo_memory[mutated_intersection.id] <= 0:
                mutations.append(
                    (candidate, mutated_intersection, candidate.evaluate(city)))
        taboo_memory = {intersection_id: max(
            0, taboo_memory[intersection_id]-1) for intersection_id in taboo_memory}
        if mutations == []:
            continue
        best_candidate = max(mutations, key=lambda x: x[2])
        current = (best_candidate[0], best_candidate[2])
        taboo_memory[best_candidate[1].id] = randint(
            0, number_of_iterations // 10)
        if current[1] > current_max[1]:
            current_max = current
        print(current[1])
    return current_max
