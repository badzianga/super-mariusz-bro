from pickle import dump, load
from time import time

from pygame import Surface
from pygame.font import Font
from pygame.image import load as load_image
from pygame.math import Vector2
from pygame.mixer import Sound, music
from pygame.sprite import Group
from pygame.time import Clock

from .coin import SpinningCoin
from .constants import (BG_COLOR, BLACK, GAME_OVER_STATE, LEVEL_STATE,
                        LOADING_STATE, MENU_STATE, WHITE)
from .debris import Debris
from .debug import Debug
from .fireball import Fireball
from .hud import Hud
from .level import Level
from .player import Mariusz
from .points import Points
from .powerups import FireFlower, Mushroom, OneUP


class Controller:
    """
    Object responsible for controlling (almost) whole game. It creates all
    necessary objects (Player, Level, HUD, etc.) and updates them.
    Pausing, adding points, coins and lifes - it's all here.
    """

    def __init__(self, screen: Surface, clock: Clock) -> None:
        "Initialize Controller - 'brain' of the game."
        self.screen = screen
        self.font = Font('fonts/PressStart2P.ttf', 8)

        # player variables
        self.lifes = 3
        self.coins = 0
        self.points = 0
        self.world = 1
        self.player_size = 0

        # level variable
        self.scroll = 0

        # spaghetti
        self.worlds = {
            1: '1-1',
            1.5: '1-1_extra'
        }
        self.themes = {
            1: 'red',
            1.5: 'blue'
        }
        self.bg_colors = {
            1: BG_COLOR,
            1.5: BLACK
        }
        self.theme = self.themes[self.world]
        self.music = {
            1: 'music/smb_supermariobros.mp3',
            1.5: 'music/smb_underground.mp3',
        }
        self.music_hurry = {
            1: 'music/smb_supermariobroshurry.mp3',
            1.5: 'music/smb_undergroundhurry.mp3',
        }
        self.checkpoint = (1320, 184)  # TODO: this is used only for 1-1 for now

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
        self.level = Level(screen, self.worlds[self.world], self.theme)
        player_pos = self.level.load_level(
            self.create_spinning_coin, self.add_coin, self.create_debris,
            self.add_powerup
        )
        self.player = Mariusz(screen, player_pos, 0, self.add_coin,
                              self.add_points, self.create_fireball,
                              self.remove_life, self.switch_state,
                              self.add_life)
        self.hud = Hud(screen, int(self.world), self.theme, self.font)

        # groups
        self.enemies = self.level.enemies
        self.floating_points = Group()
        self.coins_group = self.level.coins
        self.tiles_group = self.level.tiles
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

        self.paused = False  # if game is paused

        # Okay, now I'm doing some spaghetti. It's my first time with these
        self.states = {
            MENU_STATE: self.menu_state,
            LOADING_STATE: self.loading_state,
            LEVEL_STATE: self.level_state,
            GAME_OVER_STATE: self.game_over_state
        }
        self.current_state = MENU_STATE
        self.switch_time = time()  # TODO: change this later

        # TODO: this might be temporary
        self.screen = screen
        self.menu_image = load_image('img/menu.png').convert()

        # load highscore
        try:
            with open('highscore', 'rb') as f:
                self.highscore = load(f)
        except FileNotFoundError:
            self.highscore = 0
            with open('highscore', 'wb') as f:
                dump(self.highscore, f)

        # more spaghetti
        # these are 'portals' between maps - special colliders on pipes
        self.portals = {
            1: (928, 128, 'down'),
            1.5: (206, 199, 'right')
        }
        # TODO: change this in the future, for now it will work
        self.previous_level = None
        self.checkpoint = False

    def reset_level(self, change_level: bool=False) -> None:
        self.player_size = self.player.size
        # TEMPORARY!!!
        self.theme = self.themes[self.world]

        music.load(self.music[self.world])
        music.play(-1)
        # the most important objects
        self.level = Level(self.screen, self.worlds[self.world], self.theme)
        player_pos = self.level.load_level(
            self.create_spinning_coin, self.add_coin, self.create_debris,
            self.add_powerup
        )
        self.player = Mariusz(self.screen, player_pos, self.player_size, self.add_coin,
                              self.add_points, self.create_fireball,
                              self.remove_life, self.switch_state,
                              self.add_life)
        if not change_level:
            self.hud = Hud(self.screen, int(self.world), self.theme, self.font)
            # TODO: proper checkpoint (why I'm even doing this)
            if self.world == 1 and self.checkpoint:
                self.player.rect.x = 1320
                self.player.pos.x = 1320
                self.player.rect.y = 184
                self.player.pos.y = 184
        else:
            # TODO: change this in the future, for now it will work
            if self.world == 1 and self.previous_level == 1.5:
                # pipe exit
                self.player.rect.x = 2616
                self.player.pos.x = 2616
                self.player.rect.y = 152
                self.player.pos.y = 152

        # groups
        self.enemies = self.level.enemies
        self.floating_points = Group()
        self.coins_group = self.level.coins
        self.tiles_group = self.level.tiles
        self.powerups = Group()
        self.fireballs = Group()

        self.dont_change_music = False
        self.paused = False  # if game is paused
        self.switch_time = time()  # TODO: change this later
        self.scroll = 0  # TODO: apply checkpoint scroll if needed

    def reset_game(self) -> None:
        self.reset_level()
        self.lifes = 3
        self.coins = 0
        self.points = 0
        self.world = 1
        # TODO: here for now
        self.previous_level = None
        self.checkpoint = False

    def add_powerup(self, position: tuple, oneup: bool=False) -> None:
        """Generate proper power-up and add it to power-ups group."""
        if oneup:
            self.powerups.add(OneUP(self.images['1up'], position))
            return
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
        if type(amount) == int:
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

    def menu_state(self, _) -> None:
        """Update and draw all things related to menu."""

        self.screen.blit(self.menu_image, (0, 0))
        surf = self.font.render(str(self.highscore).zfill(6), False, WHITE)
        self.screen.blit(surf, (136, 176))

        self.hud.update(self.coins, self.points)
        self.hud.update_coin_indicator()

        self.hud.draw()

    def loading_state(self, _) -> None:
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

        self.screen.fill(self.bg_colors[self.world])  # clear screen Surface
        self.level.draw(self.scroll)  # draw all tiles
        
        # update floating points, spinning coins and debris
        self.floating_points.update(dt)

        # this section is skipped when player is dead or took power-up
        if self.player.is_alive and not self.player.is_upgrading:
            # update positions
            self.powerups.update(dt, self.tiles_group)
            self.fireballs.update(dt, self.tiles_group, self.enemies)
            self.enemies.update(dt, self.tiles_group, self.enemies,
                                self.scroll)
            if self.player.update(dt, self.coins_group, self.tiles_group,
                                  self.enemies, self.powerups, self.scroll,
                                  self.portals[self.world]):
                self.previous_level = self.world
                if isinstance(self.world, int):
                    self.world += 0.5
                else:
                    self.world = int(self.world - 0.5)
                self.reset_level(change_level=True)

            # TODO: proper checkpoint, for now this will work
            if self.player.rect.x >= 1320:
                self.checkpoint = True

            # update HUD content - points, coins and time
            self.hud.update(self.coins, self.points)
            self.hud.update_timer()

            # play hurry music
            if self.hud.timer == 100:
                if not self.dont_change_music:
                    music.load(self.music_hurry[self.world])
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
            enemy.draw(self.screen, self.scroll)
        for points in self.floating_points:
            points.draw(self.screen, self.scroll)
        self.player.draw(self.scroll)
        self.hud.draw()
        self.coins_group.update(self.screen, self.scroll)
        for powerup in self.powerups:
            powerup.draw(self.screen, self.scroll)
        self.tiles_group.update()
        for fireball in self.fireballs:
            fireball.draw(self.screen, self.scroll)

        # update scroll
        if isinstance(self.world, float):
            return  # I don't want to update scroll when on extra map
        if self.player.rect.x - 128 >= self.scroll:
            self.scroll = self.player.rect.x - 128

    def game_over_state(self, _) -> None:
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
            self.hud.update_world(int(self.world))
            self.hud.half_reset()
            self.switch_time = time()
        elif self.current_state == LEVEL_STATE:
            self.reset_level()  # TEMPORARY
        elif self.current_state == GAME_OVER_STATE:
            music.load('music/smb_gameover.wav')
            music.play()
            self.switch_time = time()
            # save score
            if self.points > self.highscore:
                with open('highscore', 'wb') as f:
                    dump(self.points, f)
                    self.highscore = self.points
        elif self.current_state == MENU_STATE:
            self.reset_game()

    def run(self, dt: float) -> None:
        """Run current state."""
        self.states[self.current_state](dt)

        # temporary, I'm using it only during development
        self.debug.draw()
