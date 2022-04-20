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

        self.genetic_params = ["Number of Generations",
                               "Population Size",
                               "Subpopulation Size",
                               "Mutation Probability"]

        self.tabu_params = ["Number of Iterations",
                            "Number of Mutations per Iteration",
                            "Max Worse Jump Percentage"]

        self.annealing_params = ["Number of Iterations"]

        self.ils_params = ["Number of Iterations",
                           "Number of Mutations per Interation"]

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

            option = self.get_option("Enter an option: ")
            if option == -1:
                err = True
                continue

            match option:
                case 0:
                    return
                case 1:
                    params = self.get_params(self.genetic_params)
                    if params == []:
                        continue

                    # genetic_algorithm(city=0, number_of_generations=0, population_size = 0, subpopulation_size = 0, mutation_chance = 0)
                case 2:
                    params = self.get_params(self.tabu_params)
                    if params == []:
                        continue

                    # taboo_search(city=0,number_of_iterations=0,number_of_mutations_per_iteration=0,max_worse_jump_percentage=0)
                case 3:
                    params = self.get_params(self.annealing_params)
                    if params == []:
                        continue

                    # annealing
                case 4:
                    params = self.get_params(self.ils_params)
                    if params == []:
                        continue

                    # iterated_local_search(city=0,number_of_iterations=0,number_of_mutations_per_iteration=0)
                case 5:
                    # city = City.from_input("traffic_signaling/asset/data/e.txt")
                    # schedule = genetic_algorithm(city, 50, 300, 50, 0.05)
                    # iterated_local_search(city,50,schedule)
                    continue
                case _:
                    print("Input option not valid")
                    err = True

    def get_params(self, params_list):
        params = []

        for i in range(len(params_list)):
            while 1:
                print()
                print(params_list[i], ": (To exit type 0)")
                param = self.get_option("Input value: ")
                if param == -1:
                    continue
                elif param == 0:
                    return []
                elif param > 0:
                    params.append(param)
                    break
                print("Invalid Number")
        return 0

    def get_city(self):
        return 0

    def get_option(self, msg):
        try:
            option = int(input(msg))
            return option
        except:
            print("Invalid input")
        return -1

    def print_menu(self):
        print()
        print(self.title, '\n')
        for i in range(len(self.menu)):
            print(i+1, "-", self.menu[i])
        print()
        print("0 - EXIT")
