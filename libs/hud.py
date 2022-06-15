from math import ceil
from time import time

from pygame.constants import SRCALPHA
from pygame.font import Font
from pygame.image import load as load_image
from pygame.surface import Surface

from .constants import BLACK, TRANSPARENT, WHITE


class Hud:
    """
    Class responsible for displaying points, coins, current world and time.
    It doesn't have logic to kill Mariusz when time is up or add extra life
    after collecting 100 coins. It only shows information.
    """

    def __init__(self, screen: Surface, world: int, theme: str,
                 font: Font) -> None:
        """Initialize HUD."""
        self.screen = screen
        self.last_time = time()
        self.font = font

        self.timer = 400

        self.labels = (  # labels and their positions
            (self.font.render('MARIUSZ', False, WHITE), (8, 0)),
            (self.font.render('WORLD', False, WHITE), (128, 0)),
            (self.font.render('TIME', False, WHITE), (184, 0))
        )

        # coin indicator stuff
        self.coin_surfs = [  # coin images used for animation
            load_image(f'img/{theme}/mini_coin_{i}.png').convert_alpha()
            for i in range(3)
        ]
        self.coin_surf = self.coin_surfs[0]
        self.coin_animation = [(0, 0.45), (1, 0.15), (2, 0.15), (1, 0.15)]
        self.coin_frame = 0
        self.coin_timer = time()

        self.world = None  # later it'll be a rendered Surface
        self.update_world(world)  # create Surface with world number

        self.loading_screen_coin = load_image('img/blue/mini_coin_0.png').convert()
        self.mariusz_sprite = load_image('img/idle_0.png').convert()
        self.x_mark = load_image('img/x_mark.png')

        # HUD surface for easier positioning
        self.surface = Surface((224, 16), SRCALPHA)
        # surface used for loading screen
        # this one doesn't have to be transparent
        self.loading_screen_surface = Surface((71, 41))

    def draw(self) -> None:
        """"Draw HUD onto screen."""
        self.screen.blit(self.surface, (16, 8))

    def half_reset(self) -> None:
        """Reset timer, set current coin frame to 0 and change coin ... TODO"""
        self.timer = 400

        self.coin_frame = 0
        self.coin_timer = time()

    def update_world(self, world: int) -> None:
        """
        Update Surface with world and map number. This method should be called
        during map changing."""
        # calculate map number
        if world % 4 == 0:
            second_number = 4
        else:
            second_number = world % 4

        # update Surface with world and map number
        self.world = self.font.render(
            f'{ceil(world / 4)}-{second_number}', False, WHITE
        )

    def update_coin_indicator(self) -> None:
        """
        Update coin indicator animation - it's a standalone method because it
        should also be updated after death.
        """
        if time() - self.coin_timer >= self.coin_animation[self.coin_frame][1]:
            self.coin_timer = time()
            self.coin_frame += 1
            if self.coin_frame >= 4:
                self.coin_frame = 0

        coin_surface = self.coin_surfs[self.coin_animation[self.coin_frame][0]]
        self.surface.blit(coin_surface, (72, 8))

    def draw_loading_screen_exclusive(self, lifes: int) -> None:
        """Draw different coin indicator and lifes."""
        # indicator
        self.surface.blit(self.loading_screen_coin, (72, 8))

        # clear loading_screen-exclusive surface
        self.loading_screen_surface.fill(BLACK)

        # world
        self.loading_screen_surface.blit(self.labels[1][0], (0, 0))
        self.loading_screen_surface.blit(self.world, (48, 0))
        self.loading_screen_surface.blit(self.mariusz_sprite, (8, 25))

        # mariusz
        self.surface.blit(self.mariusz_sprite, (80, 89))
        self.loading_screen_surface.blit(self.x_mark, (33, 34))
        surf = self.font.render(str(lifes), False, WHITE)
        self.loading_screen_surface.blit(surf, (56, 32))

        # draw surface onto screen
        self.screen.blit(self.loading_screen_surface, (88, 72))

    def draw_game_over_screen_exclusive(self) -> None:
        """Draw different coin indicator and game over text."""
        # indicator
        self.surface.blit(self.loading_screen_coin, (72, 8))

        # game over text
        surf = self.font.render('GAME OVER', False, WHITE)
        self.screen.blit(surf, (88, 120))

    def update_timer(self) -> None:
        """Update timer and draw it onto HUD surface."""
        if time() - self.last_time >= 0.4:
                self.timer = max(self.timer - 1, 0)
                self.last_time = time()

        # display time
        surf = self.font.render(str(self.timer).zfill(3), False, WHITE)
        self.surface.blit(surf, (192, 8))

    def update(self, coins: int, points: int) -> None:
        """
        Update HUD content - world, coins and points. Coin indicator and timer
        are updated separately.
        """
        # clear hud
        self.surface.fill(TRANSPARENT)

        # display labels
        for label, pos in self.labels:
            self.surface.blit(label, pos)

        # display coins amount
        surf = self.font.render(f'x{str(coins).zfill(2)}', False, WHITE)
        self.surface.blit(surf, (80, 8))

        # display points
        surf = self.font.render(str(points).zfill(6), False, WHITE)
        self.surface.blit(surf, (8, 8))

        # display world
        self.surface.blit(self.world, (136 , 8))
