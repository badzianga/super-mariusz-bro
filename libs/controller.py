from pygame import Surface
from pygame.mixer import music
from pygame.time import Clock

from .constants import BG_COLOR
from .debug import Debug
from .hud import Hud
from .level import Level
from .player import Mariusz


class Controller:
    def __init__(self, screen: Surface, clock: Clock) -> None:
        self.screen = screen

        self.level = Level(screen)
        self.player = Mariusz(screen, 40, 184)
        self.hud = Hud(screen)

        self.debug = Debug(screen, clock)

        music.load("music/smb_supermariobros.mp3")
        music.play(-1)

    def run(self, dt: float) -> None:
        self.screen.fill(BG_COLOR)
        self.level.draw()
        self.player.update(dt)
        self.hud.update()

        self.debug.draw()
