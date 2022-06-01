from time import time

from pygame.font import Font
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface

from .constants import WHITE


class Points(Sprite):
    def __init__(self, pos: tuple, amount: int) -> None:
        super().__init__()
        self.image = Font('fonts/PressStart2P.ttf', 8).render(
            str(amount), False, WHITE)
        self.rect = self.image.get_rect(topleft=pos)
        self.position = Vector2(self.rect.x, self.rect.y)
        self.timer = time()

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(self, dt: float) -> None:
        if time() - self.timer >= 1:
            self.kill()
        self.position.y += -1 * dt
        self.rect.y = self.position.y