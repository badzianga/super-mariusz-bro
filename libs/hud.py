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
    def __init__(self, screen: Surface, theme: str) -> None:
        """Initialize HUD."""
        self.screen = screen
        self.last_time = time()
        self.font = Font('fonts/PressStart2P.ttf', 8)

        self.timer = 400

        self.components = {  # labels and their positions
            'MARIUSZ': (8, 0),
            'WORLD': (128, 0),
            '1-1': (136 , 8),
            'TIME': (184, 0)
        }

        self.coin_surfs = [  # coin images used for animation
            load_image(f'img/{theme}/mini_coin_{i}.png').convert_alpha()
            for i in range(3)
        ]
        self.coin_surf = self.coin_surfs[0]
        self.coin_animation = [(0, 0.45), (1, 0.15), (2, 0.15), (1, 0.15)]
        self.coin_frame = 0
        self.coin_timer = time()

        # HUD surface for easier positioning
        self.surface = Surface((224, 16), SRCALPHA)

    def draw(self) -> None:
        """"Draw HUD onto screen."""
        self.screen.blit(self.surface, (16, 8))

    def update(self, coins: int, points: int) -> None:
        """Update HUD content - coin animation, coins, points and time."""
        # clear hud
        self.surface.fill(TRANSPARENT)

        # display labels
        for text, pos in self.components.items():
            surf = self.font.render(text, False, WHITE)
            self.surface.blit(surf, pos)

        # display coin indicator
        if time() - self.coin_timer >= self.coin_animation[self.coin_frame][1]:
            self.coin_timer = time()
            self.coin_frame += 1
            if self.coin_frame >= 4:
                self.coin_frame = 0
        coin_surface = self.coin_surfs[self.coin_animation[self.coin_frame][0]]
        self.surface.blit(coin_surface, (72, 8))

        # display coins amount
        if coins < 10:
            surf = self.font.render(f'x0{coins}', False, WHITE)
        else:
            surf = self.font.render(f'x{coins}', False, WHITE)
        self.surface.blit(surf, (80, 8))

        # display points
        zeros = 6-len(str(points))
        surf = self.font.render(f'{"0" * zeros}{points}', False, WHITE)
        self.surface.blit(surf, (8, 8))
        
        # update timer
        if time() - self.last_time >= 0.4:
            self.timer = max(self.timer - 1, 0)
            self.last_time = time()

        # display time
        surf = self.font.render(str(self.timer), False, WHITE)
        self.surface.blit(surf, (192, 8))

        self.draw()
