# TODO: self.size variable which holds player.size between levels
# TODO: save and load high score. Display it in the menu

from time import time

from pygame import Surface
from pygame.image import load as load_image
from pygame.math import Vector2
from pygame.mixer import Sound, music
from pygame.sprite import Group
from pygame.time import Clock

from .coin import Coin, SpinningCoin
from .constants import (BG_COLOR, BLACK, GAME_OVER_STATE, LEVEL_STATE,
                        LOADING_STATE, MENU_STATE)
from .debris import Debris
from .debug import Debug
from .enemies import Goomba, Koopa
from .fireball import Fireball
from .hud import Hud
from .level import Level
from .player import Mariusz
from .points import Points
from .powerups import FireFlower, Mushroom


class Controller:
    """
    Object responsible for controlling (almost) whole game. It creates all
    necessary objects (Player, Level, HUD, etc.) and updates them.
    Pausing, adding points, coins and lifes - it's all here.
    """

    def __init__(self, screen: Surface, clock: Clock) -> None:
        "Initialize Controller - 'brain' of the game."
        self.screen = screen

        # player variables
        self.lifes = 3
        self.coins = 0
        self.points = 0
        self.world = 1

        # most of the images will be loaded here in the future
        self.images = {
            'mushroom': load_image('img/mushroom.png'),
            '1up': load_image('img/1up_mushroom.png'),
            'debris': load_image('img/red/debris.png'),
            'fire_flower': tuple([
                load_image(f'img/flower_{i}.png').convert_alpha()
                for i in range(4)
            ]),
            'fireball': tuple([
                load_image(f'img/fireball_{i}.png').convert_alpha()
                for i in range(7)
            ])
        }

        # the most important objects
        self.level = Level(screen)
        self.level.load_level(self.create_spinning_coin, self.add_coin,
                              self.create_debris, self.add_powerup)
        self.player = Mariusz(screen, (32, 64), 0, self.add_coin,
                              self.add_points, self.create_fireball,
                              self.remove_life, self.switch_state)
        self.hud = Hud(screen, self.world, 'red')

        # groups
        self.enemies = Group(Goomba(176, 144, 'red'), Goomba(200, 144, 'red'),
                             Koopa(224, 144))
        self.floating_points = Group()
        self.coins_group = Group(Coin((83, 184), 'red'))
        self.powerups = Group()
        self.fireballs = Group()

        # sounds
        self.pause_sound = Sound('sfx/smb_pause.wav')
        self.coin_sound = Sound('sfx/smb_coin.wav')
        self.oneup_sound = Sound('sfx/smb_1-up.wav')
        self.fireball_sound = Sound('sfx/smb_fireball.wav')

        # debug object, used to display useful info during development
        self.debug = Debug(screen, clock)

        # when timer is 100, music is changed a few times whis is unwanted
        # that's why this switch is needed
        self.dont_change_music = False
        # TODO: set dont_change_music to True somewhere

        self.paused = False  # if game is paused

        # Okay, now I'm doing some spaghetti. It's my first time with these
        self.states = {
            MENU_STATE: self.menu_state,
            LOADING_STATE: self.loading_state,
            LEVEL_STATE: self.level_state,
            GAME_OVER_STATE: self.game_over_state
        }
        self.current_state = LEVEL_STATE
        self.switch_time = time()  # TODO: change this later

        # TODO: this might be temporary
        self.screen = screen
        self.menu_image = load_image('img/menu.png').convert()

    def reset_level(self) -> None:
        # TEMPORARY!!!

        # the most important objects
        self.level = Level(self.screen)
        self.level.load_level(self.create_spinning_coin, self.add_coin,
                              self.create_debris, self.add_powerup)
        self.player = Mariusz(self.screen, (32, 64), 0, self.add_coin,
                              self.add_points, self.create_fireball,
                              self.remove_life, self.switch_state)
        self.hud = Hud(self.screen, self.world, 'red')

        # groups
        self.enemies = Group(Goomba(176, 144, 'red'), Goomba(200, 144, 'red'),
                             Koopa(224, 144))
        self.floating_points = Group()
        self.coins_group = Group(Coin((83, 184), 'red'))
        self.powerups = Group()
        self.fireballs = Group()

        self.dont_change_music = False
        self.paused = False  # if game is paused
        self.switch_time = time()  # TODO: change this later

    def reset_game(self) -> None:
        self.reset_level()
        self.lifes = 3
        self.coins = 0
        self.points = 0
        self.world = 1

    def add_powerup(self, position: tuple) -> None:
        """Generate proper power-up and add it to power-ups group."""
        if self.player.size == 0:
            self.powerups.add(Mushroom(self.images['mushroom'], position))
        else:
            self.powerups.add(FireFlower(self.images['fire_flower'], position))

    def add_coin(self) -> None:
        """Add coin and handle all its' consequences."""
        self.coins += 1
        self.points += 200
        if self.coins >= 100:
            self.coins -= 100
            self.add_life()
            return  # if life is added, coin sound shouldn't be played
        self.coin_sound.play()

    def add_points(self, amount: int, create_sprite: bool=True) -> None:
        """
        Add points and create floating points sprite.
        This method should be called after killing enemies and collecting
        power-ups.
        """
        # I'm also using this method from create_debris
        # breaking bricks wouldn't create points sprite
        self.points += amount
        if create_sprite:
            # TODO: position above killed enemy, not player
            # I can add position as argument, but it's for later
            pos = list(self.player.rect.topleft)
            pos[0] -= 8
            self.create_floating_points(pos, amount)

    def create_floating_points(self, position: tuple, amount: int) -> None:
        """Create floating points sprite and add it to the group."""
        self.floating_points.add(Points(position, amount))

    def create_fireball(self, position: tuple, direction: int) -> None:
        self.fireballs.add(Fireball(self.images['fireball'], position,
                                    direction, self.add_points))
        self.fireball_sound.play()

    def add_life(self) -> None:
        """Add life and play 1UP sound."""
        self.lifes += 1
        self.oneup_sound.play()

    def remove_life(self) -> None:
        """Remove life after death."""
        self.lifes -= 1

    def create_spinning_coin(self, position: tuple) -> None:
        """Create spinning coin from question block."""
        self.floating_points.add(
            SpinningCoin(position, self.create_floating_points)
        )

    def create_debris(self, pos: tuple) -> None:
        """Create brick fragments from destroying brick."""
        self.floating_points.add(
            Debris((pos[0] - 8, pos[1] - 8), self.images['debris'], Vector2(-1, -12), False),
            Debris((pos[0] + 8, pos[1] - 8), self.images['debris'], Vector2(1, -12), True),
            Debris((pos[0] - 8, pos[1] + 8), self.images['debris'], Vector2(-1, -10), False),
            Debris((pos[0] + 8, pos[1] + 8), self.images['debris'], Vector2(1, -10), True)
        )
        self.add_points(50, False)

    def pause(self) -> None:
        """Pause game and music. Also play pausing sound."""
        self.paused = not self.paused
        self.pause_sound.play()
        if music.get_busy():
            music.pause()
        else:
            music.unpause()

    def menu_state(self, dt: float) -> None:
        """Update and draw all things related to menu."""

        self.screen.blit(self.menu_image, (0, 0))

        self.hud.update(self.coins, self.points)
        self.hud.update_coin_indicator()

        self.hud.draw()

    def loading_state(self, dt: float) -> None:
        """Update and draw all objects and groups related to loading screen."""
        if time() - self.switch_time >= 3:
            self.switch_state(LEVEL_STATE)
            return

        self.screen.fill(BLACK)

        self.hud.update(self.coins, self.points)
        self.hud.draw_loading_screen_exclusive(self.lifes)

        self.hud.draw()

    def level_state(self, dt: float) -> None:
        """Update and draw all objects and groups related to level."""
        if self.paused:  # don't update game if paused
            return

        self.screen.fill(BG_COLOR)  # clear whole screen Surface
        self.level.draw()  # draw all tiles
        
        # update floating points, spinning coins and debris
        self.floating_points.update(dt)

        # this section is skipped when player is dead or took power-up
        if self.player.is_alive and not self.player.is_upgrading:
            # update positions
            self.powerups.update(dt, self.level.tiles)
            self.fireballs.update(dt, self.level.tiles, self.enemies)
            self.enemies.update(dt, self.level.tiles, self.enemies)
            self.player.update(dt, self.coins_group, self.level.tiles,
                               self.enemies, self.powerups)

            # update HUD content - points, coins and time
            self.hud.update(self.coins, self.points)
            self.hud.update_timer()

            # play hurry music
            if self.hud.timer == 100:
                if not self.dont_change_music:
                    music.load('music/smb_supermariobroshurry.mp3')
                    music.play()
                self.dont_change_music = True

            # kill player when time expires
            elif self.hud.timer == 0:
                self.player.kill()

        # update upgrade animation - when player took power-up 
        elif self.player.is_upgrading:
            self.player.upgrade_animation()
        # update die animation when player is dead
        else:
            self.player.die_animation(dt)

        # update coin indicator animation
        # it's independent because it should be updated e.g. after death
        self.hud.update_coin_indicator()

        # draw objects onto screen Surface
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.floating_points.draw(self.screen)
        self.player.draw()
        self.hud.draw()
        self.coins_group.update(self.screen)
        self.powerups.draw(self.screen)
        self.level.tiles.update()
        self.fireballs.draw(self.screen)

    def game_over_state(self, dt: float) -> None:
        """Update and draw all things related to game over screen."""

        self.screen.fill(BLACK)

        self.hud.update(self.coins, self.points)
        self.hud.draw_game_over_screen_exclusive()

        self.hud.draw()

        if time() - self.switch_time >= 7:
            self.switch_state(MENU_STATE)

    def switch_state(self, state: int) -> None:
        """Swich current game state. Used in children objects, e.g. Player."""
        if self.lifes > 0 or state == MENU_STATE:
            self.current_state = state
        else:
            self.current_state = GAME_OVER_STATE
    
        if self.current_state == LOADING_STATE:
            music.pause()
            self.hud.update_world(self.world)
            self.hud.half_reset()
            self.switch_time = time()
        elif self.current_state == LEVEL_STATE:
            self.reset_level()  # TEMPORARY
            music.load('music/smb_supermariobros.mp3')
            music.play(-1)
        elif self.current_state == GAME_OVER_STATE:
            music.load('music/smb_gameover.wav')
            music.play()
            self.switch_time = time()
        elif self.current_state == MENU_STATE:
            self.reset_game()

    def run(self, dt: float) -> None:
        """Run current state."""

        self.states[self.current_state](dt)

        # temporary, I'm using it only during development
        self.debug.draw()
