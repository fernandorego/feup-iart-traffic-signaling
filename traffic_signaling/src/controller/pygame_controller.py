from time import sleep
import pygame
from model.city import City
from controller.city_controller import CityController
from model.schedule import Schedule

WINDOW_SIZE = (1300, 800)


class PygameController:
    def __init__(self, city: City, schedule: Schedule) -> None:
        self.window_size = WINDOW_SIZE
        self.window = self.init_pygame()
        self.city_controller = CityController(
            city, schedule, self.window, WINDOW_SIZE)
        self.main()

    def init_pygame(self) -> None:
        pygame.init()
        return pygame.display.set_mode(self.window_size)

    def quit_pygame(self) -> None:
        pygame.quit()

    def is_running(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_pygame()

    def main(self) -> None:
        self.city_controller.simulate()

    def update(self) -> None:
        self.city_controller.update()
