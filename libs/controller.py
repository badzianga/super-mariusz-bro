import pygame

from .player import Mariusz


class Controller:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font("fonts/PressStart2P.ttf", 8)

        self.player = Mariusz(self.screen, 32, 32)

    def run(self, dt: float) -> None:
        self.player.draw()