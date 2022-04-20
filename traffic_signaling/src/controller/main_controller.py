from model.city import City
from model.schedule import Schedule
from controller.city_controller import CityController
from controller.pygame_controller import PygameController
from algorithm.local_search import iterated_local_search
from algorithm.taboo import taboo_search
from algorithm.genetics import genetic_algorithm

from random import seed


class MainController:
    def __init__(self) -> None:
        self.title = "Traffic Signaling - Hash Code Problem"
        self.menu = ["Genetic Algorithm", "Tabu Search", "Simulated Annealing",
                     "Iterated Local Search", "Automatic Mode"]

    def main_loop(self):
        # seed()
        # city = City.from_input("traffic_signaling/asset/data/e.txt")
        # schedule = iterated_local_search(city, 50, 5)
        # schedule[0].write_to_file(".", "my_solution")
        option = 0
        err = False
        while 1:
            if not err:
                err = False
                self.print_menu()

            option = self.get_option()
            if option == -1:
                err = True
                continue

            match option:
                case 0:
                    return
                case 1:
                    # genetic_algorithm(city=0, number_of_generations=0, population_size = 0, subpopulation_size = 0, mutation_chance = 0)
                    continue
                case 2:
                    # taboo_search(city=0,number_of_iterations=0,number_of_mutations_per_iteration=0,max_worse_jump_percentage=0)
                    continue
                case 3:
                    # annealing
                    continue
                case 4:
                    # iterated_local_search(city=0,number_of_iterations=0,number_of_mutations_per_iteration=0)
                    continue
                case 5:
                    # city = City.from_input("traffic_signaling/asset/data/e.txt")
                    # schedule = genetic_algorithm(city, 50, 300, 50, 0.05)
                    # iterated_local_search(city,50,schedule)
                    continue
                case _:
                    print("Input option not valid")
                    err = True

    def get_genetic_params(self):
        return 0

    def get_tabu_params(self):
        return 0

    def get_annealing_params(self):
        return 0

    def get_ils_params(self):
        return 0

    def get_city(self):
        return 0

    def get_option(self):
        try:
            option = int(input("Enter an option: "))
            return option
        except:
            print("Invalid input")
        return -1

    def print_menu(self):
        print(self.title, '\n')
        for i in range(len(self.menu)):
            print(i+1, "-", self.menu[i])
        print()
        print("0 - EXIT")
