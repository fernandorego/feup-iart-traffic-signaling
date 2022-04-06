from model.city import City
from model.schedule import Schedule
from model.intersection import Intersection
from random import randint


def generate_random_solution(city: City):
    schedule = Schedule()

    for _, (intersection_id, intersection) in enumerate(city.intersections.items()):
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


def generate_communist_random_solution(city: City):
    schedule = Schedule()

    for _, (intersection_id, intersection) in enumerate(city.intersections.items()):
        schedule.schedule[intersection_id] = []

        intersection_schedule = {
            street.name: 1 for street in intersection.incoming_streets
        }
        intersection_remaining_time = city.duration - len(intersection_schedule)

        for street in intersection.incoming_streets:
            street_green_light_time = randint(0, intersection_remaining_time)

            if street_green_light_time > 0:

                intersection_remaining_time -= street_green_light_time

                intersection_schedule[street.name] += street_green_light_time

            if intersection_remaining_time == 0:
                break

        for street_name, street_time in intersection_schedule.items():
            schedule.schedule[intersection_id] += [
                street_name for _ in range(street_time)
            ]

    return schedule
