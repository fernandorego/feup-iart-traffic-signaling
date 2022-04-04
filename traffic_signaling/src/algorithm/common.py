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
                
                if not(intersection_has_schedule):
                    schedule.schedule[intersection_id] = []
                    intersection_has_schedule = True
                
                intersection_remaining_time -= street_green_light_time
                schedule.schedule[intersection_id] += [street.name for _ in range(street_green_light_time)]
            
            if intersection_remaining_time == 0:
                break

    return schedule