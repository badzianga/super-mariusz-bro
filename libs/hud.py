from pygame.constants import SRCALPHA
from pygame.font import Font
from pygame.surface import Surface

from .constants import WHITE


class Hud:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.font = Font("fonts/PressStart2P.ttf", 8)

        self.components = {
            "MARIUSZ": (8, 0),
            "000000": (8, 8),
            "x00": (80, 8),
            "WORLD": (128, 0),
            "1-1": (136 , 8),
            "TIME": (184, 0),
            "400": (192, 8)
        }
        self.surface = Surface((224, 16), SRCALPHA)

    def draw(self) -> None:
        self.screen.blit(self.surface, (16, 8))

    def update(self) -> None:
        for text, pos in self.components.items():
            surf = self.font.render(text, False, WHITE)
            self.surface.blit(surf, pos)

        self.draw()
