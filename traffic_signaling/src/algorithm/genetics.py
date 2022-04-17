from random import randint, random
from multiprocessing import Process, Queue, Manager
from math import ceil
from toolz import unique

import os

from model.city import City
from model.schedule import Schedule
from .common import (
    generate_random_solution,
    distributed_sum_permutation,
    random_sum_permutation,
)


def genetic_algorithm_process(
    city: City,
    number_of_generations: int,
    population_size: int,
    mutation_chance: float,
    result: Queue,
):

    population = [
        generate_random_solution(city, distributed_sum_permutation)
        for _ in range(population_size)
    ]

    print(f"Starting process {os.getpid()} with a population of size {population_size}")

    genetic_map = {}
    for schedule in population:
        schedule.evaluate(city)
        genetic_map = genetic_mapping(schedule, genetic_map)

    for _ in range(number_of_generations):
        for schedule in population:
            if random() <= mutation_chance:
                schedule = mutate_single_street(city, schedule)
                schedule.evaluate(city)

        for index in range(int(len(population) / 4)):
            best_parent = population[index]
            second_parent_index = index
            while second_parent_index == index:
                second_parent_index = randint(0, len(population) - 1)

            random_parent = population[second_parent_index]

            child_1, child_2 = cross_over(
                city,
                randint(0, len(city.intersections) - 1),
                best_parent,
                random_parent,
            )

            child_1.evaluate(city)
            child_2.evaluate(city)
            population.append(child_1)
            population.append(child_2)

        population.sort(
            key=lambda x: x.last_score
            + genetic_evaluation(x, genetic_map, city.car_value),
            reverse=True,
        )
        population = population[: population_size + 1]

        genetic_map = {}
        for schedule in population:
            genetic_map = genetic_mapping(schedule, genetic_map)

        print(
            f"Process {os.getpid()} at iteration {_ + 1} scored an average of {sum([x.last_score for x in population]) / len(population)}"
        )

    print([x.last_score for x in population])

    result.put(population)
    return None


def genetic_algorithm(
    city: City,
    number_of_generations: int,
    population_size: int,
    subpopulation_size: int,
    mutation_chance: float,
):
    population = []
    processes = []
    result = Manager().Queue()
    remaining = population_size
    subpopulation = subpopulation_size

    for _ in range(ceil(population_size / subpopulation_size)):
        if remaining < subpopulation_size:
            subpopulation = remaining
        processes.append(
            Process(
                target=genetic_algorithm_process,
                args=(
                    city,
                    number_of_generations,
                    subpopulation,
                    mutation_chance,
                    result,
                ),
            )
        )

        remaining -= subpopulation_size

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    for _ in processes:
        population.extend(result.get())

    genetic_map = {}
    for schedule in population:
        genetic_map = genetic_mapping(schedule, genetic_map)

    population = list(unique(population, key=lambda x: x.last_score))
    population.sort(
        key=lambda x: x.last_score + genetic_evaluation(x, genetic_map, city.car_value),
        reverse=True,
    )

    print()
    print("### Final Population Scores ###")
    print([x.last_score for x in population])
    print()

    for _ in range(number_of_generations):
        for schedule in population:
            if random() <= mutation_chance:
                schedule = mutate_single_street(city, schedule)
                schedule.evaluate(city)

        for index in range(int(len(population) / 4)):
            best_parent = population[index]
            second_parent_index = index
            while second_parent_index == index:
                second_parent_index = randint(0, len(population) - 1)

            random_parent = population[second_parent_index]

            child_1, child_2 = cross_over(
                city,
                randint(0, len(city.intersections) - 1),
                best_parent,
                random_parent,
            )

            child_1.evaluate(city)
            child_2.evaluate(city)
            population.append(child_1)
            population.append(child_2)

        population.sort(
            key=lambda x: x.last_score,
            reverse=True,
        )
        population = population[: population_size + 1]

        print(
            f"Generation {_ + 1} scored an average of {sum([x.last_score for x in population]) / len(population)}"
        )

    print([x.last_score for x in population])
    return None


def genetic_evaluation(schedule: Schedule, genetic_mapping: dict, car_bonus: int):
    score = 0

    for intersection_id, intersection_schedule in schedule.schedule.items():
        if not (intersection_id in genetic_mapping.keys()):
            score += car_bonus * 2
            continue
        streets = set(intersection_schedule)
        for street in streets:
            if not (street in genetic_mapping[intersection_id].keys()):
                score += car_bonus * 2
                continue
            street_time = intersection_schedule.count(street)

            if not (street_time in genetic_mapping[intersection_id][street].keys()):
                score += car_bonus * 2
                continue
            elif genetic_mapping[intersection_id][street][street_time] == min(
                genetic_mapping[intersection_id][street].values()
            ):
                score += car_bonus
    return score


def genetic_mapping(schedule: Schedule, mapping: dict):
    for intersection_id, intersection_schedule in schedule.schedule.items():
        if not (intersection_id in mapping.keys()):
            mapping[intersection_id] = {}
        streets = set(intersection_schedule)
        for street in streets:
            if not (street in mapping[intersection_id].keys()):
                mapping[intersection_id][street] = {}
            street_time = intersection_schedule.count(street)
            if not (street_time in mapping[intersection_id][street].keys()):
                mapping[intersection_id][street][street_time] = 1
            else:
                mapping[intersection_id][street][street_time] += 1
    return mapping


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


def mutate_random_intersection(city: City, schedule: Schedule):
    intersections = list(enumerate(city.intersections.items()))
    _, (intersection_id, intersection) = intersections[
        randint(0, len(intersections) - 1)
    ]

    intersection_schedule = distributed_sum_permutation(
        len(intersection.incoming_streets), city.duration
    )
    schedule.schedule[intersection_id] = []

    for index, street in enumerate(intersection.incoming_streets):
        schedule.schedule[intersection_id] += [
            street.name for _ in range(intersection_schedule[index])
        ]
    return schedule


def mutate_single_street(city: City, schedule: Schedule):
    intersections = list(city.intersections.keys())
    intersection_id = intersections[randint(0, len(intersections) - 1)]
    current_intersection_schedule = schedule.schedule[intersection_id]

    current_intersection_schedule_dict = {
        street_name: current_intersection_schedule.count(street_name)
        for street_name in set(current_intersection_schedule)
    }

    streets = list(current_intersection_schedule_dict.items())
    if len(streets) > 1:
        street, street_time = streets[randint(0, len(streets) - 1)]
    else:
        street, street_time = streets[0]

    remaining_time = city.duration - (
        sum(list(current_intersection_schedule_dict.values())) - street_time
    )

    current_intersection_schedule_dict[street] = randint(0, remaining_time)

    schedule.schedule[intersection_id] = [
        street_name
        for street_name, street_time in current_intersection_schedule_dict.items()
        for _ in range(street_time)
    ]

    return schedule
