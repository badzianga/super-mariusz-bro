from pygame import Surface
from pygame.mixer import music

from .player import Mariusz
from .level import Level
from .hud import Hud


class Controller:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen

        self.level = Level(screen)
        self.player = Mariusz(screen, 40, 184)
        self.hud = Hud(screen)

        music.load("music/smb_supermariobros.mp3")
        music.play(-1)

    def run(self, dt: float) -> None:
        self.level.draw()
        self.player.update(dt)
        self.hud.update()