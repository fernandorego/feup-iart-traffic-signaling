from math import log, exp
from model.city import City
from model.schedule import Schedule
from .common import distributed_sum_permutation, generate_random_solution, mutate_single_street

def simulated_annealing(city: City):
    t = 0
    
    current_schedule = generate_random_solution(city, distributed_sum_permutation)
    current_schedule.evaluate(city)

    while True:
        print(f"For t = {t}, simulated annealing reached a score of {current_schedule.last_score}")
        T = scheduling_function(t)
        if T <= 0:
            return current_schedule
        next_schedule = mutate_single_street(city, current_schedule)
        next_schedule.evaluate(city)

        score_diff = next_schedule.last_score - current_schedule.last_score

        if score_diff > 0 or exp(-score_diff / T):
            current_schedule = next_schedule
        
        print(f"Current T = {T}, Probability = {exp(-score_diff / T)}, Score_diff = {score_diff}")
        t += 1
        

def scheduling_function(t: float, T0=100):
    return T0 / (1 + log(1 + t))