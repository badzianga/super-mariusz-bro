import pygame

from .constants import WHITE


class Controller:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font("fonts/PressStart2P.ttf", 8)

    def run(self, dt: float) -> None:
        pass