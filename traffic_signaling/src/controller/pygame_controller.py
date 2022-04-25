import pygame
from model.city import City
from controller.city_controller import CityController
from model.schedule import Schedule
from time import time, sleep

WINDOW_SIZE = (1300, 800)
FPS = 30


class PygameController:
    def __init__(self, city: City) -> None:
        """
        Constructor of PygameController class

        Properties:
            window_size (tuple): tuple with width and height of pygame window
            window (Surface): pygame window for display
            city_controller (CityController): city controller used to simulate a solution
        """
        self.window_size = WINDOW_SIZE
        self.window = self.init_pygame()
        self.city_controller = CityController(
            city, self.window, WINDOW_SIZE)

    def init_pygame(self) -> None:
        """
        Pygame and screen initialization 

        Return:
            Pygame Surface to display
        """
        pygame.init()
        return pygame.display.set_mode(self.window_size)

    def quit_pygame(self) -> None:
        '''Unitialize all pygame modules'''
        pygame.quit()

    def simulate(self, schedule: Schedule) -> None:
        '''Simulation of a possible solution to view in pygame'''
        self.city_controller.set_schedule(schedule)
        if self.city_controller.simulate() == 1:
            self.quit_pygame()
        self.wait_for_exit()

    def wait_for_exit(self) -> None:
        '''Wait for an event (press ESQ or close the window) to quit pygame'''
        start = time()
        while self.is_running():
            sleep(max(1.0/FPS - (time() - start), 0))
            continue
        self.quit_pygame()

    def is_running(self) -> bool:
        """
        Check if does not exist at least one of the following events: press ESQ or close the window

        Return:
            False if the events exist, True otherwise 
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
        return True
