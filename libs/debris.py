from time import time

from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.transform import flip as flip_image

from .constants import DISPLAY_SIZE


class Debris(Sprite):
    def __init__(self, position: tuple, image: Surface, speed: Vector2,
                 flip: bool) -> None:
        super().__init__()

        self.image = flip_image(image, False, flip)
        self.last_time = time()

        self.rect = self.image.get_rect(center=position)
        self.pos = Vector2(position)
        self.speed = speed

    def update(self, dt: float) -> None:
        if time() - self.last_time >= 0.1:
            self.image = flip_image(self.image, False, True)
            self.last_time = time()

        self.speed.y = min(self.speed.y + 1 * dt, 8)

        self.pos.x += self.speed.x * dt
        self.rect.x = self.pos.x

        self.pos.y += self.speed.y * dt
        self.rect.y = self.pos.y

        if self.pos.y > DISPLAY_SIZE[1]:
            self.kill()
