import pygame
from model.city import City
from controller.city_controller import CityController
from model.schedule import Schedule

WINDOW_SIZE = (1300, 800)


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

    def is_running(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_pygame()

    def simulate(self, schedule) -> None:
        self.city_controller.set_schedule(schedule)
        if self.city_controller.simulate() == 1:
            self.quit_pygame()

    def update(self) -> None:
        self.city_controller.update()
