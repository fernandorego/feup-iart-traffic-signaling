from model.city import City
from model.schedule import Schedule
#from common import generate_random_solution

def genetic_algorithm(city: City, number_of_generations: int, population_size: int, mutation_chance: float):
    return


def cross_over(city: City, cross_over_point: int, parent_1: Schedule, parent_2: Schedule):
    child_1, child_2 = Schedule(), Schedule()
    for index, (intersection_id, _) in enumerate(city.intersections.items()):
        if intersection_id in parent_1.schedule.keys():
            if index >= cross_over_point:
                child_2.schedule[intersection_id] = parent_1.schedule[intersection_id]
            else:
                child_1.schedule[intersection_id] = parent_1.schedule[intersection_id]

        if intersection_id in parent_2.schedule.keys():
            if index >= cross_over_point:
                child_1.schedule[intersection_id] = parent_2.schedule[intersection_id]
            else:
                child_2.schedule[intersection_id] = parent_2.schedule[intersection_id]
                

    return child_1, child_2
