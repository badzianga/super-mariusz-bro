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
from .points import Points


class Controller:
    def __init__(self, screen: Surface, clock: Clock) -> None:
        self.screen = screen

        # player variables
        self.lifes = 3
        self.coins = 0
        self.points = 0
        self.world = 1

        self.level = Level(screen)
        self.player = Mariusz(screen, 32, 64, self.add_coin,
                              self.add_points_from_enemy)
        self.hud = Hud(screen, self.world, 'red')

        self.enemies = Group(Goomba(176, 144, 'red'))

        self.floating_points = Group()

        self.coins_group = Group(Coin((83, 184), 'red'), Coin((99, 184), 'red'))
        self.debug = Debug(screen, clock)

        self.dont_change_music = False
        self.pausing = False

        music.load('music/smb_supermariobros.mp3')
        music.play(-1)

        self.pause_sound = Sound('sfx/smb_pause.wav')
        self.coin_sound = Sound('sfx/smb_coin.wav')
        self.oneup_sound = Sound('sfx/smb_1-up.wav')

    def add_coin(self) -> None:
        self.coins += 1
        self.points += 200
        if self.coins >= 100:
            self.coins -= 100
            self.add_life()
            return
        self.coin_sound.play()

    def add_points_from_enemy(self, amount: int) -> None:
        self.points += amount
        self.floating_points.add(Points(self.player.rect.topleft, amount))

    def add_life(self) -> None:
        self.lifes += 1
        self.oneup_sound.play()

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
        self.floating_points.update(dt)

        if self.player.is_alive:
            self.enemies.update(dt, self.level.tiles)

            self.player.update(dt, self.coins_group, self.level.tiles,
                               self.enemies)

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

        self.hud.update_coin_indicator()

        self.enemies.draw(self.screen)
        self.floating_points.draw(self.screen)
        self.player.draw()
        self.hud.draw()

        self.coins_group.update(self.screen)
        self.level.tiles.update()
        self.debug.draw()
