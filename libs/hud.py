from math import ceil
from time import time

from pygame.constants import SRCALPHA
from pygame.font import Font
from pygame.image import load as load_image
from pygame.surface import Surface

from .constants import TRANSPARENT, WHITE


class Hud:
    """
    Class responsible for displaying points, coins, current world and time.
    It doesn't have logic to kill Mariusz when time is up or add extra life
    after collecting 100 coins. It only shows information.
    """

    def __init__(self, screen: Surface, world: int, theme: str) -> None:
        """Initialize HUD."""
        self.screen = screen
        self.last_time = time()
        self.font = Font('fonts/PressStart2P.ttf', 8)

        self.timer = 400

        self.labels = (  # labels and their positions
            (self.font.render('MARIUSZ', False, WHITE), (8, 0)),
            (self.font.render('WORLD', False, WHITE), (128, 0)),
            (self.font.render('TIME', False, WHITE), (184, 0))
        )

        self.coin_surfs = [  # coin images used for animation
            load_image(f'img/{theme}/mini_coin_{i}.png').convert_alpha()
            for i in range(3)
        ]
        self.coin_surf = self.coin_surfs[0]
        self.coin_animation = [(0, 0.45), (1, 0.15), (2, 0.15), (1, 0.15)]
        self.coin_frame = 0
        self.coin_timer = time()

        self.world = None
        self.update_world(world)

        # HUD surface for easier positioning
        self.surface = Surface((224, 16), SRCALPHA)

    def draw(self) -> None:
        """"Draw HUD onto screen."""
        self.screen.blit(self.surface, (16, 8))

    def update_world(self, world: int):
        if world % 4 == 0:
            second_number = 4
        else:
            second_number = world % 4
        self.world = self.font.render(
            f'{ceil(world / 4)}-{second_number}', False, WHITE
        )

    def update_coin_indicator(self) -> None:
        """
        Update coin indicator animation - it's a standalone method because it
        should also be updated after death
        """
        if time() - self.coin_timer >= self.coin_animation[self.coin_frame][1]:
            self.coin_timer = time()
            self.coin_frame += 1
            if self.coin_frame >= 4:
                self.coin_frame = 0
        coin_surface = self.coin_surfs[self.coin_animation[self.coin_frame][0]]
        self.surface.blit(coin_surface, (72, 8))

    def update(self, coins: int, points: int) -> None:
        """
        Update HUD content - world, coins, points and time. Coin indicator is
        updated separately.
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
        
        # update timer
        if time() - self.last_time >= 0.4:
            self.timer = max(self.timer - 1, 0)
            self.last_time = time()

        # display time
        surf = self.font.render(str(self.timer), False, WHITE)
        self.surface.blit(surf, (192, 8))

        # display world
        self.surface.blit(self.world, (136 , 8))
