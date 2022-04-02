import pygame
import time
from model.city import City
from controller.city_controller import CityController
from view.city_viewer import CityViewer

WINDOW_SIZE = (1300, 700)
BG_COLOR = (255, 255, 255)
FPS = 1


class PygameController:
    def __init__(self, city) -> None:
        self.window_size = WINDOW_SIZE
        self.fps = FPS
        self.bg_color = BG_COLOR
        self.city_controller = CityController(city)
        self.city_viewer = CityViewer(city)
        self.window = self.init_pygame()
        self.main()

    def init_pygame(self) -> None:
        pygame.init()
        return pygame.display.set_mode(self.window_size)

    def quit_pygame(self) -> None:
        pygame.quit()

    def loop(self) -> None:
        run = True
        while run and self.bg_color[2] > 10:

            start = time.time()
            run = self.is_running()

            self.update()
            self.draw()

            self.set_bg_color(
                self.bg_color[0], self.bg_color[1], self.bg_color[2]-50)

            time.sleep(max(1.0/self.fps - (time.time() - start), 0))

        pygame.quit()

    def is_running(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def set_bg_color(self, r, g, b) -> None:
        self.bg_color = (r, g, b)

    def main(self) -> None:
        self.loop()

        self.quit_pygame()

    def update(self) -> None:
        self.city_controller.update()

    def draw(self) -> None:
        self.window.fill(self.bg_color)

        self.city_viewer.draw(self.window)

        pygame.display.flip()
