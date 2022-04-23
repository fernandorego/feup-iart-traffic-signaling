from model.city import City
from model.schedule import Schedule
from controller.pygame_controller import PygameController
from algorithm.local_search import iterated_local_search, print_ils_results_graph_from_file
from algorithm.taboo import taboo_search, print_taboo_results_graph_from_file
from algorithm.genetics import genetic_algorithm, print_genetic_results_graph_from_file
from algorithm.annealing import simulated_annealing, print_sa_results_graph_from_file
from algorithm.common import mutate_schedule, mutate_intersection, mutate_single_street

EXPORT_PATH = "traffic_signaling/asset/out"


class MainController:
    def __init__(self) -> None:
        """
        Constructor of MainController class

        Properties:
            title (string): main title of the program
            menu (list): options list for the main menu of the program 
            genetic_params (list): list of params (integers) for the genetic algorithm 
            genetic_params2 (list): list of params (floats) for the genetic algorithm
            tabu_params (list): list of params (integers) for the tabu search
            annealing_params (list): list of params (integers) for the simulated annealing algorithm
            ils_params (list): list of params (integers) for the iterative local search
            cities (list): list of available cities
        """
        self.title = "Traffic Signaling - Hash Code Problem"
        self.menu = ["Genetic Algorithm", "Tabu Search", "Simulated Annealing",
                     "Iterated Local Search"]

        self.genetic_params = ["Number of Generations",
                               "Population Size",
                               "Subpopulation Size"]

        self.genetic_params2 = ["Mutation Probability"]

        self.tabu_params = ["Number of Iterations",
                            "Number of Mutations per Iteration"]

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
        '''Main loop of the program which provides a clean interface for the user'''
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
                    params2 = self.get_params_float(self.genetic_params2)
                    if params == [] or params2 == []:
                        continue
                    city = self.get_city()
                    schedule = genetic_algorithm(city, params[0], params[1],
                                                 params[2], params2[0])
                    print_genetic_results_graph_from_file()
                    schedule.write_to_file(
                        EXPORT_PATH, 'genetic_last_solution.txt')
                case 2:
                    params = self.get_params(self.tabu_params)
                    if params == []:
                        continue
                    city = self.get_city()
                    schedule: Schedule = taboo_search(
                        city, params[0], params[1])
                    print_taboo_results_graph_from_file()
                    schedule.write_to_file(
                        EXPORT_PATH, 'tabu_last_solution.txt')
                case 3:
                    params = self.get_params(self.annealing_params)
                    if params == []:
                        continue
                    city = self.get_city()
                    iteration_mutation_pairs = [(params[0], lambda x: mutate_schedule(city, x, 0.5)), (
                        params[0], lambda x: mutate_intersection(city, x)[0]), (params[0], lambda x: mutate_single_street(city, x))]
                    schedule: Schedule = simulated_annealing(
                        city, iteration_mutation_pairs)
                    print_sa_results_graph_from_file()
                    schedule.write_to_file(
                        EXPORT_PATH, 'sim_annealing_last_solution.txt')
                case 4:
                    params = self.get_params(self.ils_params)
                    if params == []:
                        continue
                    city = self.get_city()
                    schedule: Schedule = iterated_local_search(
                        city, params[0], params[1])
                    print_ils_results_graph_from_file()
                    schedule.write_to_file(
                        EXPORT_PATH, 'ils_last_solution.txt')
                case _:
                    print("Input option not valid")
                    err = True
                    continue

            if city.no_intersections < 15:
                controller = PygameController(city)
                controller.simulate(schedule)

    def get_params(self, params_list):
        """
        Get an integer given by the user for each param in params_list.

        Parameters:
            params_list (list): List of parameters to get from the user

        Return:
            list with the input given by the user
        """
        params = []

        for i in range(len(params_list)):
            while 1:
                print()
                print(params_list[i], ": (To exit type 0)")
                param = self.get_option("-> ")
                if param == -1:
                    continue
                elif param == 0:
                    return []
                elif param > 0:
                    params.append(param)
                    break
                print("Invalid Number")
        return params

    def get_params_float(self, params_list):
        """
        Get an float given by the user for each param in params_list.

        Parameters:
            params_list (list): List of parameters to get from the user

        Return:
            list with the input given by the user
        """
        params = []

        for i in range(len(params_list)):
            while 1:
                print()
                print(
                    params_list[i], ": (To exit type 0)")
                param = self.get_option_float("interval: (0.0, 1.0] -> ")
                if param == -1:
                    continue
                elif param == 0:
                    return []
                elif param > 0 and param <= 1:
                    params.append(param)
                    break
                print("Invalid Number")
        return params

    def get_city(self):
        """
        Print all accessible cities and returns the city chosen by the user.

        Return:
            City chosen by the user
        """
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
        """
        Get a integer number from the user

        Parameters:
            msg (string): message to show when user input is requested
        """
        try:
            option = int(input(msg))
            return option
        except:
            print("Invalid input")
        return -1

    def get_option_float(self, msg):
        """
        Get a float number from the user

        Parameters:
            msg (string): message to show when user input is requested
        """
        try:
            option = float(input(msg))
            return option
        except:
            print("Invalid input")
        return -1

    def print_menu(self):
        '''Print the main menu'''
        print()
        print(self.title, '\n')
        for i in range(len(self.menu)):
            print(i+1, "-", self.menu[i])
        print()
        print("0 - EXIT")
