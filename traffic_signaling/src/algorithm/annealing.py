from copy import deepcopy
from math import log, exp
from random import random
from model.city import City
from .common import distributed_sum_permutation, generate_random_solution, random_sum_permutation

def simulated_annealing(city: City, iteration_mutation_pairs: list):
    t = 0
    
    current_schedule = generate_random_solution(city, random_sum_permutation)
    current_schedule.evaluate(city)
    print(current_schedule)

    for number_of_iterations, mutation_operator in iteration_mutation_pairs:
        for _ in range(number_of_iterations):
            print(f"For t = {t}, simulated annealing reached a score of {current_schedule.last_score}")
            T = scheduling_function(t)
            if T <= 0:
                break
            next_schedule = mutation_operator(deepcopy(current_schedule))
            next_schedule.evaluate(city)

            score_diff = next_schedule.last_score - current_schedule.last_score

            print(f"Current T = {T}, Probability = {exp(score_diff / T)}, Score_diff = {score_diff}")

            if score_diff > 0 or random() < exp(score_diff / T):
                current_schedule = next_schedule
            
            t += 1
        
    print(current_schedule)
    return current_schedule

def scheduling_function(t: float, T0=3000):
    return T0 / (1 + log(1 + t))