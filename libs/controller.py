import pygame

from .player import Mariusz
from .constants import WHITE


class Controller:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font("fonts/PressStart2P.ttf", 8)

        self.player = Mariusz(self.screen, 32, 32)

    def run(self, dt: float) -> None:
        surf = self.font.render("MARIUSZ", False, WHITE)
        self.player.update(dt)
        self.screen.blit(surf, (32, 16))