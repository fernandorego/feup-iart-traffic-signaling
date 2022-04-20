from model.city import City
from model.schedule import Schedule
from controller.city_controller import CityController
from controller.pygame_controller import PygameController
from algorithm.local_search import iterated_local_search
from algorithm.taboo import taboo_search
from algorithm.genetics import genetic_algorithm
from algorithm.annealing import simulated_annealing

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

        self.cities = ["City A - 4 intersections",
                       "City B - 7073 intersections",
                       "City C - 10000 intersections",
                       "City D - 8000 intersections",
                       "City E - 500 intersections",
                       "City F - 1662 intersections"]

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
                    city = self.get_city()
                    genetic_algorithm(city, params[0], params[1],
                                      params[2], params[3])
                case 2:
                    params = self.get_params(self.tabu_params)
                    if params == []:
                        continue
                    city = self.get_city()
                    taboo_search(city, params[0], params[1], params[2])
                case 3:
                    params = self.get_params(self.annealing_params)
                    if params == []:
                        continue
                    city = self.get_city()
                    simulated_annealing(city, params[0])
                case 4:
                    params = self.get_params(self.ils_params)
                    if params == []:
                        continue
                    city = self.get_city()
                    iterated_local_search(city, params[0], params[1])
                case 5:
                    city = self.get_city()
                    schedule = genetic_algorithm(city, 75, 300, 50, 0.05)
                    schedule.write_to_file('.', 'bruno')
                    schedule = iterated_local_search(city, 300, 75, schedule)
                    schedule.write_to_file('.', 'nando')
                    print(schedule.last_score)
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
        return params

    def get_city(self):
        print()
        for i in range(len(self.cities)):
            print(i+1, "-", self.cities[i])

        err = False

        while 1:
            if not err:
                err = False

            option = self.get_option("Enter an option: ")

            match option:
                case 0: return None
                case 1: return City.from_input("traffic_signaling/asset/data/a.txt")
                case 2: return City.from_input("traffic_signaling/asset/data/b.txt")
                case 3: return City.from_input("traffic_signaling/asset/data/c.txt")
                case 4: return City.from_input("traffic_signaling/asset/data/d.txt")
                case 5: return City.from_input("traffic_signaling/asset/data/e.txt")
                case 6: return City.from_input("traffic_signaling/asset/data/f.txt")
                case _:
                    print("Input option not valid")
                    err = True

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
