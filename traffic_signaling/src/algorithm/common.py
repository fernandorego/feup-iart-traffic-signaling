from model.city import City
from model.schedule import Schedule
from model.intersection import Intersection
from random import randint


def generate_random_solution(city: City, schedule_generator):
    schedule = Schedule()

    for intersection_id, intersection in city.intersections.items():
        intersection_schedule = schedule_generator(
            len(intersection.incoming_streets), city.duration
        )
        schedule.schedule[intersection_id] = []

        for index, street in enumerate(intersection.incoming_streets):
            schedule.schedule[intersection_id] += [
                street.name for _ in range(intersection_schedule[index])
            ]

    return schedule


def random_sum_permutation(length: int, perm_sum: int):
    permutation = [0 for _ in range(length)]
    while perm_sum > 0:
        temp = randint(0, perm_sum)
        perm_sum -= temp
        permutation[randint(0, length - 1)] += temp
    return permutation


def distributed_sum_permutation(length: int, perm_sum: int):
    if length > perm_sum:
        return [1 if index < perm_sum else 0 for index in range(length)]

    permutation = [1 for _ in range(length)]
    perm_sum -= length
    while perm_sum > 0:
        temp = randint(0, perm_sum)
        perm_sum -= temp
        permutation[randint(0, length - 1)] += temp
    return permutation
