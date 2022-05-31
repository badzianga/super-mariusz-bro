from pygame import Surface
from pygame.mixer import music
from pygame.time import Clock

from .constants import BG_COLOR
from .debug import Debug
from .hud import Hud
from .level import Level
from .player import Mariusz
from .coin import Coin
from pygame.sprite import Group


class Controller:
    def __init__(self, screen: Surface, clock: Clock) -> None:
        self.screen = screen

        # player variables
        self.lifes = 3
        self.coins = 0
        self.points = 0
        self.world = 1

        self.level = Level(screen)
        self.player = Mariusz(screen, 40, 64, self.add_coin, self.reset_coins)
        self.hud = Hud(screen, self.world, "red")

        self.coins_group = Group(Coin((84, 184), "red"), Coin((100, 184), "red"))
        self.debug = Debug(screen, clock)

        self.dont_change_music = False

        music.load("music/smb_supermariobros.mp3")
        music.play(-1)

    def add_coin(self) -> int:
        self.coins += 1
        self.points += 200
        return self.coins

    def reset_coins(self) -> None:
        self.coins -= 100
        self.lifes += 1

    def run(self, dt: float) -> None:
        self.screen.fill(BG_COLOR)
        self.level.draw()
        self.player.update(dt, self.coins_group, self.level.tiles)

        self.hud.update(self.coins, self.points)

        if self.hud.timer == 100:
            if self.dont_change_music:
                return
            music.load("music/smb_supermariobroshurry.mp3")
            music.play()
            self.dont_change_music = True

        self.coins_group.update(self.screen)
        self.debug.draw()
