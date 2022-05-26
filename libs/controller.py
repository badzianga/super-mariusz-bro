from pygame import Surface, SRCALPHA
from pygame.font import Font

from .player import Mariusz
from .constants import WHITE


class Controller:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.font = Font("fonts/PressStart2P.ttf", 8)

        self.player = Mariusz(self.screen, 32, 32)

        self.hud = Surface((224, 16), SRCALPHA)
        self.hud_components = {
            "MARIUSZ": (8, 0),
            "000000": (8, 8),
            "x00": (80, 8),
            "WORLD": (128, 0),
            "1-1": (128 , 8),
            "TIME": (184, 0),
            "400": (184, 8)
        }
        self.update_hud()

    def update_hud(self):
        for text, pos in self.hud_components.items():
            surf = self.font.render(text, False, WHITE)
            self.hud.blit(surf, pos)

    def run(self, dt: float) -> None:
        self.player.update(dt)

        self.screen.blit(self.hud, (16, 8))