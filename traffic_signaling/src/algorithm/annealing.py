from copy import deepcopy
from math import log, exp
from model.city import City
from model.schedule import Schedule
from .common import distributed_sum_permutation, generate_random_solution, mutate_single_street

def simulated_annealing(city: City, number_of_iterations: int):
    t = 0
    
    current_schedule = generate_random_solution(city, distributed_sum_permutation)
    current_schedule.evaluate(city)

    for t in range(number_of_iterations):
        print(f"For t = {t}, simulated annealing reached a score of {current_schedule.last_score}")
        T = scheduling_function(t)
        if T <= 0:
            return current_schedule
        next_schedule = mutate_single_street(city, current_schedule)
        next_schedule.evaluate(city)

        score_diff = next_schedule.last_score - current_schedule.last_score

        if score_diff > 0 or exp(-score_diff / T):
            current_schedule = deepcopy(next_schedule) # por algum motivo, isto não faz deepcopy
        
        print(f"Current T = {T}, Probability = {exp(-score_diff / T)}, Score_diff = {score_diff}") # debug
        

def scheduling_function(t: float, T0=500):
    return T0 / (1 + log(1 + t))