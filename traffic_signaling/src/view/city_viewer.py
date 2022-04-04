import pygame
from model.city import City


class CityViewer:
    def __init__(self, city: City) -> None:
        self.city = city

    def draw(self, window) -> None:
        font = pygame.font.SysFont(None, 24)

        for id, intersection in self.city.intersections.items():
            pygame.draw.circle(window, (85, 156, 173),
                               intersection.get_pos(), 20.0)
            img = font.render(str(id), True, (255, 94, 91))
            window.blit(img, (intersection.get_pos()[0] - 5,
                              intersection.get_pos()[1] - 7))
