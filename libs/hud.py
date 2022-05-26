from time import time

from pygame.constants import SRCALPHA
from pygame.font import Font
from pygame.surface import Surface
from pygame.image import load as load_image

from .constants import WHITE, TRANSPARENT


class Hud:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.timer = 400
        self.last_time = time()
        self.font = Font("fonts/PressStart2P.ttf", 8)

        self.components = {
            "MARIUSZ": (8, 0),
            "000000": (8, 8),
            "x00": (80, 8),
            "WORLD": (128, 0),
            "1-1": (136 , 8),
            "TIME": (184, 0)
        }
        self.coin_surface = load_image("img/mini_coin.png").convert_alpha()
        self.surface = Surface((224, 16), SRCALPHA)

    def draw(self) -> None:
        self.screen.blit(self.surface, (16, 8))

    def update(self) -> None:
        self.surface.fill(TRANSPARENT)
        for text, pos in self.components.items():
            surf = self.font.render(text, False, WHITE)
            self.surface.blit(surf, pos)

        # display coin
        self.surface.blit(self.coin_surface, (72, 8))

        # update timer
        if time() - self.last_time > 0.4:
            self.timer = max(self.timer - 1, 0)
            self.last_time = time()

        # display time
        surf = self.font.render(str(self.timer), False, WHITE)
        self.surface.blit(surf, (192, 8))

        self.draw()
