from model.city import City
from model.schedule import Schedule
from random import randint, random


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
    permutation = [1 for _ in range(length)]
    while perm_sum > 0 and 1 in permutation:
        temp, index = randint(0, perm_sum), randint(0, length - 1)
        if permutation[index] != 1 or perm_sum - temp < 0:
            continue
        perm_sum -= temp
        permutation[index] += temp
    return permutation


def distributed_sum_permutation(length: int, perm_sum: int):
    if length > perm_sum:
        return random_sum_permutation(length, perm_sum)

    return [1 for _ in range(length)]


def mutate_intersection(city: City, schedule: Schedule) -> tuple[Schedule, int]:
    intersections = list(enumerate(city.intersections.items()))
    _, (intersection_id, intersection) = intersections[
        randint(0, len(intersections) - 1)
    ]

    intersection_schedule = random_sum_permutation(
        len(intersection.incoming_streets), city.duration
    )
    schedule.schedule[intersection_id] = []

    for index, street in enumerate(intersection.incoming_streets):
        schedule.schedule[intersection_id] += [
            street.name for _ in range(intersection_schedule[index])
        ]

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
        streets = list(city.intersections[intersection_id].incoming_streets)
        street, street_time = streets[randint(0, len(streets) - 1)].name, 0

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


def mutate_schedule(city, schedule, strength):
    another_solution = generate_random_solution(city, random_sum_permutation)
    return mix_solutions(city, schedule, another_solution, strength)


def mix_solutions(city, base_schedule, foreigner_schedule, probability):
    perturbation = Schedule()
    for j in range(city.no_intersections):
        r = random()
        if r < probability:
            perturbation.schedule[j] = foreigner_schedule.schedule[j]
        else:
            perturbation.schedule[j] = base_schedule.schedule[j]
    return perturbation
