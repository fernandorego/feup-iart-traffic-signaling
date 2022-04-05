from random import randint, random

from model.city import City
from model.schedule import Schedule
from .common import generate_random_solution
from collections import deque

# from common import generate_random_solution


def genetic_algorithm(
    city: City, number_of_generations: int, population_size: int, mutation_chance: float
):
    print("Generating initial solutions...")
    population = deque(generate_random_solution(city) for _ in range(population_size))

    for _ in range(number_of_generations):
        print("Creating generation ", _, "...")
        for couple in range(0, population_size, 2):
            child_1, child_2 = cross_over(
                city,
                randint(0, city.no_intersections - 1),
                population[couple],
                population[couple + 1],
            )
            if random() <= mutation_chance:
                population[couple] = mutate_intersection(city, population[couple])
            if random() <= mutation_chance:
                population[couple + 1] = mutate_intersection(
                    city, population[couple + 1]
                )

            if child_1.evaluate(city) > population[0].evaluate(city):
                population.popleft()
                population.append(child_1)
            if child_2.evaluate(city) > population[0].evaluate(city):
                population.popleft()
                population.append(child_2)

    print([x.evaluate(city) for x in population])
    return population[0]


def cross_over(
    city: City, cross_over_point: int, parent_1: Schedule, parent_2: Schedule
):
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

    return [child_1, child_2]


def mutate_intersection(city: City, schedule: Schedule):
    intersections = list(enumerate(city.intersections.items()))
    _, (intersection_id, intersection) = intersections[
        randint(0, len(intersections) - 1)
    ]

    intersection_remaining_time = city.duration
    intersection_has_schedule = False

    for street in intersection.incoming_streets:
        street_green_light_time = randint(0, intersection_remaining_time)

        if street_green_light_time > 0:

            if not (intersection_has_schedule):
                schedule.schedule[intersection_id] = []
                intersection_has_schedule = True

            intersection_remaining_time -= street_green_light_time
            schedule.schedule[intersection_id] += [
                street.name for _ in range(street_green_light_time)
            ]

        if intersection_remaining_time == 0:
            break
    return schedule
