from pygame import Surface
from pygame.mixer import Sound, music
from pygame.sprite import Group
from pygame.time import Clock

from .coin import Coin
from .constants import BG_COLOR
from .debug import Debug
from .enemies import Goomba
from .hud import Hud
from .level import Level
from .player import Mariusz


class Controller:
    def __init__(self, screen: Surface, clock: Clock) -> None:
        self.screen = screen

        # player variables
        self.lifes = 3
        self.coins = 0
        self.points = 0
        self.world = 1

        self.level = Level(screen)
        self.player = Mariusz(screen, 32, 64, self.add_coin, self.reset_coins)
        self.hud = Hud(screen, self.world, 'red')

        self.enemies = Group(Goomba(176, 144, 'red'))

        self.coins_group = Group(Coin((83, 184), 'red'), Coin((99, 184), 'red'))
        self.debug = Debug(screen, clock)

        self.dont_change_music = False
        self.pausing = False

        music.load('music/smb_supermariobros.mp3')
        music.play(-1)

        self.pause_sound = Sound('sfx/smb_pause.wav')

    def add_coin(self) -> int:
        self.coins += 1
        self.points += 200
        return self.coins

    def reset_coins(self) -> None:
        self.coins -= 100
        self.lifes += 1

    def pause(self) -> None:
        self.pausing = not self.pausing
        self.pause_sound.play()
        if music.get_busy():
            music.pause()
        else:
            music.unpause()

    def run(self, dt: float) -> None:
        if self.pausing:
            return

        self.screen.fill(BG_COLOR)
        self.level.draw()

        if self.player.is_alive:
            self.enemies.update(dt, self.level.tiles)

            self.player.update(dt, self.coins_group, self.level.tiles, self.enemies)

            self.hud.update(self.coins, self.points)

            if self.hud.timer == 100:
                if not self.dont_change_music:
                    music.load('music/smb_supermariobroshurry.mp3')
                    music.play()
                self.dont_change_music = True
            elif self.hud.timer == 0:
                self.player.kill()
        else:
            self.player.die_animation(dt)

        self.enemies.draw(self.screen)
        self.player.draw()
        self.hud.draw()

        self.coins_group.update(self.screen)
        self.debug.draw()
