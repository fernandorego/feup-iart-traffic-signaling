from model.city import City
from model.schedule import Schedule
from controller.city_controller import CityController
from controller.pygame_controller import PygameController
from algorithm.local_search import iterated_local_search
from algorithm.taboo import taboo_search

from random import seed


class MainController:
    def __init__(self) -> None:
        pass

    def main_loop(self):
        seed()
        city = City.from_input("traffic_signaling/asset/data/e.txt")
        schedule = iterated_local_search(city, 50, 5)
        schedule[0].write_to_file(".", "my_solution")
