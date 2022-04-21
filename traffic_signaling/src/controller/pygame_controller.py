import pygame
from model.city import City
from controller.city_controller import CityController
from model.schedule import Schedule
from time import time, sleep

WINDOW_SIZE = (1300, 800)
FPS = 30


class PygameController:
    def __init__(self, city: City) -> None:
        self.window_size = WINDOW_SIZE
        self.window = self.init_pygame()
        self.city_controller = CityController(
            city, self.window, WINDOW_SIZE)

    def init_pygame(self) -> None:
        pygame.init()
        return pygame.display.set_mode(self.window_size)

    def quit_pygame(self) -> None:
        pygame.quit()

    def simulate(self, schedule: Schedule) -> None:
        self.city_controller.set_schedule(schedule)
        if self.city_controller.simulate() == 1:
            self.quit_pygame()
        self.wait_for_exit()

    def update(self) -> None:
        self.city_controller.update()

    def wait_for_exit(self) -> None:
        start = time()
        while self.is_running():
            sleep(max(1.0/FPS - (time() - start), 0))
            continue
        self.quit_pygame()

    def is_running(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
        return True
