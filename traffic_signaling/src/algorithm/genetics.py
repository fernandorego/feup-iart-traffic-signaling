from random import randint, random
from multiprocessing import Process, Pool

from model.city import City
from model.schedule import Schedule
from .common import generate_communist_random_solution, generate_random_solution


def produce_children(city: City, index: int, mutation_chance: float, population: list):
    best_parent = population[index]
    random_parent = population[randint(index, len(population) - 1)]

    child_1, child_2 = cross_over(
        city,
        randint(0, len(city.intersections) - 1),
        best_parent,
        random_parent,
    )

    if random() <= mutation_chance:
        child_1 = mutate_intersection(city, child_1)
    child_1.evaluate(city)

    if random() <= mutation_chance:
        child_2 = mutate_intersection(city, child_2)
    child_2.evaluate(city)

    return [child_1, child_2]


def genetic_algorithm(
    city: City, number_of_generations: int, population_size: int, mutation_chance: float
):
    with Pool(processes=int(population_size / 2)) as pool:
        population = [
            generate_communist_random_solution(city) for _ in range(population_size)
        ]

        for schedule in population:
            schedule.evaluate(city)

        population = sorted(
            population,
            key=lambda x: x.last_score,
            reverse=True,
        )

        for _ in range(number_of_generations):
            children = []
            results = [
                pool.apply_async(
                    produce_children,
                    (
                        city,
                        index,
                        mutation_chance,
                        population,
                    ),
                )
                for index in range(int(len(population) / 4))
            ]

            children = [result.get() for result in results]

            for child in children:
                population.extend(child)

            population = sorted(population, key=lambda x: x.last_score, reverse=True)
            population = population[:population_size]

            print(
                f"Generation {_ + 1} scored an average of {sum([x.last_score for x in population]) / len(population)}"
            )
            print(population[0].last_score, population[1].last_score)

    print(population[0].last_score, population[1].last_score)
    return 0


def cross_over(
    city: City, cross_over_point: int, parent_1: Schedule, parent_2: Schedule
):
    child_1, child_2 = Schedule(), Schedule()
    for index, intersection_id in enumerate(city.intersections.keys()):
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
