from time import time
from types import FunctionType

from pygame.image import load as load_image
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface


class Coin(Sprite):
    """Animated static coin object visible on map."""

    def __init__(self, position: tuple, theme: str) -> None:
        """Initialize Coin object."""
        super().__init__()

        # animation and visual stuff
        self.images = tuple([
            load_image(f'img/{theme}/coin_{i}.png').convert_alpha()
            for i in range(3)
        ])
        self.frame = 0
        self.animation = ((0, 0.45), (1, 0.15), (2, 0.15), (1, 0.15))
        self.last_time = time()
        self.image = self.images[0]

        # position
        self.rect = self.image.get_rect(topleft=position)

    def update(self, screen: Surface) -> None:
        """Update animation and image, draw coin onto screen."""
        if time() - self.last_time >= self.animation[self.frame][1]:
            self.last_time = time()
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0
            self.image = self.images[self.animation[self.frame][0]]

        self.draw(screen)

    def draw(self, screen: Surface) -> None:
        """Draw coin onto screen."""
        screen.blit(self.image, self.rect)


class SpinningCoin(Sprite):
    """
    Animated dynamic coin object visible on map.
    This coin is spawned from question blocks and some bricks.
    """

    def __init__(self, position: tuple,
                 create_floating_points: FunctionType) -> None:
        """Initialize Coin object."""
        super().__init__()

        # animation and visual stuff
        self.images = tuple([
            load_image(f'img/spinning_coin_{i}.png').convert_alpha()
            for i in range(4)
        ])
        self.image = self.images[0]
        self.frame = 0
        self.total_time = time()
        self.last_time = time()

        # positioning stuff
        self.rect = self.image.get_rect(topleft=position)
        self.pos = Vector2(position[0], position[1])
        self.speed = Vector2(0, -8)

        self.create_floating_points = create_floating_points

    def update(self, dt: float) -> None:
        """Update animation and image, draw coin onto screen."""
        # apply gravity
        self.speed.y = min(self.speed.y + 1 * dt, 8)

        # update frame
        if time() - self.total_time >= 0.5:
            self.create_floating_points((self.rect.x - 8, self.rect.y), 200)
            self.kill()
        elif time() - self.last_time >= 0.05:
            self.last_time = time()
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0
            self.image = self.images[self.frame]

        # update position
        self.pos.y += self.speed.y * dt
        self.rect.y = self.pos.y
