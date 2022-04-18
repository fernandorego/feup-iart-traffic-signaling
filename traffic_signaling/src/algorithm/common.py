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
    return (schedule, intersection)

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
    elif len(streets) == 1:
        street, street_time = streets[0]
    else:
        streets = list(city.intersections[intersection_id])
        street, street_time = streets[randint(0, len(streets) - 1)], 0

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