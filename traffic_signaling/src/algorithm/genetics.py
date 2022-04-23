from cProfile import label
from .common import (
    generate_random_solution,
    mutate_schedule,
    distributed_random_sum_permutation,
)
from model.schedule import Schedule
from model.city import City
from random import randint, random
from multiprocessing import Process, Queue, Manager
from math import ceil
from toolz import unique

import numpy as np
from matplotlib import pyplot as plt

import os

PATH = "traffic_signaling/asset/out/genetic_result.csv"


def genetic_algorithm_process(
    city: City,
    number_of_generations: int,
    population_size: int,
    mutation_chance: float,
    result: Queue,
    file,
):
    """
    Genetic algorithm that generates a population of green light schedules for a given city.
    This function is intended to be called as an entry point for a child process.
    Instead of just searching for a better score, it also promotes rarer chromossomes.

    Parameters:
        city: city for which the schedules will be created
        number_of_generations: number of generations upon which the population will evolve
        population_size: max size of the population
        mutation_chance: probability of a schedule mutating from one generation to another
        result: multiprocess queue, through which the results will be passed to the parent process
        file: file where the evolution of the population will be registered. None if no register is needed
    """

    population = [
        generate_random_solution(city, distributed_random_sum_permutation)
        for _ in range(population_size)
    ]

    print(f"Starting process {os.getpid()} with a population of size {population_size}")

    genetic_map = {}
    for schedule in population:
        schedule.evaluate(city)
        genetic_map = chromossome_mapping(schedule, genetic_map)

    for generation in range(1, number_of_generations + 1):
        population = next_generation(
            city,
            population,
            population_size,
            lambda x: mutate_schedule(city, x, 0.1),
            cross_over,
            (
                lambda x: x.last_score
                + genetic_evaluation(x, genetic_map, city.car_value)
            ),
            mutation_chance,
        )

        genetic_map = {}
        for schedule in population:
            genetic_map = chromossome_mapping(schedule, genetic_map)

        average = sum([x.last_score for x in population]) / len(population)
        process = os.getpid()
        print(
            f"Process {process} at generation {generation} scored an average of {int(average)}"
        )
        if file is not None:
            file.write(f"1,{process},{generation},{average}\n")
            file.flush()

    print([x.last_score for x in population])

    result.put(population)
    return None


def genetic_algorithm(
    city: City,
    number_of_generations: int,
    population_size: int,
    subpopulation_size: int,
    mutation_chance: float,
    file_output: bool = True,
):
    """
    Genetic algorithm that generates a green light schedule for a given city.
    For a part of the algorithm, the population is divided into subpopulations which evolve in parallel.
    After number_of_generations generations have passed, the subpopulations are merged and evolve as one, for another
    number_of_generations generations.

    Parameters:
        city: city for which the schedule will be made
        number_of_generations: number of generations upon which the population will evolve
        subpopulation_size: size of separated groups of the population
        mutation_chance: probability of a schedule mutating from one generation to another
        file_output: whether the best final schedule will be saved to a file or not

    Return:
        a optimized schedule for the given city
    """
    population = []
    processes = []
    result = Manager().Queue()
    remaining = population_size
    subpopulation = subpopulation_size

    file = None
    if file_output:
        file = open("traffic_signaling/asset/out/genetic_result.csv", "w")
        file.write("PHASE,PROCESS,GENERATION,AVERAGE\n")
        file.flush()

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
                    file,
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

    chromossome_map = {}
    for schedule in population:
        chromossome_map = chromossome_mapping(schedule, chromossome_map)

    population = list(unique(population, key=lambda x: x.last_score))
    population.sort(
        key=lambda x: x.last_score
        + genetic_evaluation(x, chromossome_map, city.car_value),
        reverse=True,
    )

    print()
    print("### Merged Population Scores ###")
    print([x.last_score for x in population])
    print()

    for generation in range(1, number_of_generations + 1):
        population = next_generation(
            city,
            population,
            population_size,
            lambda x: mutate_schedule(city, x, 0.1),
            cross_over,
            (lambda x: x.last_score),
            mutation_chance,
        )

        average = sum([x.last_score for x in population]) / len(population)
        process = os.getpid()
        print(f"Generation {generation} scored an average of {average}")
        if file is not None:
            file.write(f"2,{process},{generation},{int(average)}\n")
            file.flush()

    print(f"Final population: {[x.last_score for x in population]}")
    return population[0]


def next_generation(
    city: City,
    population: list,
    population_size: int,
    mutation_operator,
    cross_over_function,
    sorting_function,
    mutation_chance: float,
):
    """
    For a given population, creates the next generation of schedules.

    Parameters:
        city: city for which the schedules were made
        population: current population
        population_size: max size of the population
        mutation_operator: function that mutates a schedule
        cross_over_function: cross over operator of the genetic algorithm
        sorting_function: function that orders the population in a ranking
        mutation_chance: probability of a schedule mutating

    Return:
        population of the next generation
    """
    for schedule in population:
        if random() <= mutation_chance:
            schedule = mutation_operator(schedule)
            schedule.evaluate(city)

    for index in range(int(len(population) / 4)):
        best_parent = population[index]
        second_parent_index = index
        while second_parent_index == index:
            second_parent_index = randint(0, len(population) - 1)

        random_parent = population[second_parent_index]

        child_1, child_2 = cross_over_function(
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
        key=sorting_function,
        reverse=True,
    )
    population = population[: population_size + 1]

    return population


def genetic_evaluation(schedule: Schedule, genetic_mapping: dict, bonus: int):
    """
    Evaluates a schedule based on how rare its genes are.
    For each rarest chromossome within the mapped chromossomes, it receives bonus points.
    For each unmapped chromossome or intersection, it receives a 2*bonus points.

    Parameters:
        schedule: schedule to be evaluated
        genetic_mapping: mapping of chromossomes
        bonus: integer value to be added to the final score on previously given conditions

    Return:
        schedule genetic score
    """
    score = 0

    for intersection_id, intersection_schedule in schedule.schedule.items():
        if not (intersection_id in genetic_mapping.keys()):
            score += bonus * 2
            continue
        streets = set(intersection_schedule)
        for street in streets:
            if not (street in genetic_mapping[intersection_id].keys()):
                score += bonus * 2
                continue
            street_time = intersection_schedule.count(street)

            if not (street_time in genetic_mapping[intersection_id][street].keys()):
                score += bonus * 2
                continue
            elif genetic_mapping[intersection_id][street][street_time] == min(
                genetic_mapping[intersection_id][street].values()
            ):
                score += bonus
    return score


def chromossome_mapping(schedule: Schedule, mapping: dict):
    """
    Maps the chromossomes of a schedule into a genetic map dictionary, which counts the occurrence of a given chromossome.
    A chromossome is considered to be the time attributed to a given street on a given intersection.

    Parameters:
        schedule: schedule whose chromosses will be mapped
        mapping: dictionary that will be updated with schedule's chromossomes

    Return:
        mapping dict updated with schedule's chromossomes
    """
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
    """
    Cross over operator for the genetic algorithm.
    Generates two children by selecting the intersections' green light cycle of a parent up to
    a cross over point, and then the ones from the other parent. The process is mirrored for each of the children.

    Parameters:
        city: city for which the parent schedules were made
        cross_over_point: cross over point of the operator
        parent_1: first parent schedule
        parent_2: second parent schedule

    Return:
        list with 2 children schedules
    """
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
    """
    Changes the green light cycle for a random intersection on a given schedule for a given city.

    Parameters:
        city: a city object
        schedule: green light schedule for the city

    Return:
        schedule with updated green light cycle
    """
    intersections = list(enumerate(city.intersections.items()))
    _, (intersection_id, intersection) = intersections[
        randint(0, len(intersections) - 1)
    ]

    intersection_schedule = distributed_random_sum_permutation(
        len(intersection.incoming_streets), city.duration
    )
    schedule.schedule[intersection_id] = []

    for index, street in enumerate(intersection.incoming_streets):
        schedule.schedule[intersection_id] += [
            street.name for _ in range(intersection_schedule[index])
        ]
    return schedule


def mutate_single_street(city: City, schedule: Schedule):
    """
    Changes the green light time for a single random street on a random intersection on a given schedule for a given city.

    Parameters:
        city: a city object
        schedule: green light schedule for the city

    Return:
        schedule with updated green light cycle
    """
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


def print_genetic_results_graph_from_file():
    with open(PATH) as f:
        metrics = [
            list(map(lambda i: i.strip("\n"), x.split(","))) for x in f.readlines()[1:]
        ]

    processes = set(int(x[1]) for x in metrics)
    xs = np.array(list(set(int(x[2]) for x in metrics if int(x[0]) == 1)))

    # First phase
    for process in processes:
        ys = np.array(
            [float(x[3]) for x in metrics if int(x[0]) == 1 and int(x[1]) == process]
        )
        if len(ys) == 0:
            continue
        plt.plot(xs, ys, label=f"Process {process}")
    plt.legend(loc="upper left", frameon=False)
    plt.title("Genetic algorithm: concurrent phase")
    plt.xlabel("Iteration")
    plt.ylabel("Solution score")
    plt.show()

    # Second phase
    plt.clf()
    ys = np.array([float(x[3]) for x in metrics if int(x[0]) == 2])
    plt.plot(xs, ys)
    plt.title("Genetic algorithm: merged population phase")
    plt.xlabel("Iteration")
    plt.ylabel("Solution score")
    plt.show()
