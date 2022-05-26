from pygame import Surface, SRCALPHA
from pygame.font import Font
from pygame.mixer import music

from .player import Mariusz
from .constants import WHITE
from .level import Level


class Controller:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.font = Font("fonts/PressStart2P.ttf", 8)

        self.level = Level(screen)
        self.player = Mariusz(screen, 32, 184)

        self.hud = Surface((224, 16), SRCALPHA)
        self.hud_components = {
            "MARIUSZ": (8, 0),
            "000000": (8, 8),
            "x00": (80, 8),
            "WORLD": (128, 0),
            "1-1": (136 , 8),
            "TIME": (184, 0),
            "400": (192, 8)
        }
        self.update_hud()

        music.load("music/smb_supermariobros.mp3")
        music.play(-1)

    def update_hud(self) -> None:
        for text, pos in self.hud_components.items():
            surf = self.font.render(text, False, WHITE)
            self.hud.blit(surf, pos)

    def run(self, dt: float) -> None:
        self.level.draw()

        self.player.update(dt)

        self.screen.blit(self.hud, (16, 8))