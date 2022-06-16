from time import time

from pygame.font import Font
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface

from .constants import WHITE


class Points(Sprite):
    """
    Points sprite which displays points amount from enemies, question blocks'
    coins and power-ups. It rises up and after some time it disappears.
    """

    def __init__(self, pos: tuple, amount: int) -> None:
        """Initialize Points object."""
        super().__init__()

        # create Surface with points 
        self.image = Font('fonts/PressStart2P.ttf', 8).render(
            str(amount), False, WHITE)

        # positioning stuff
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = Vector2(self.rect.x, self.rect.y)

        # timestamp with time when sprite appeared
        self.timer = time()

    def update(self, dt: float) -> None:
        """Update points sprite position and kill it when time expires."""
        self.pos.y += -1 * dt
        self.rect.y = self.pos.y

        if time() - self.timer >= 1:
            self.kill()
            return

    def draw(self, screen: Surface, scroll: int):
        """Draw sprite onto screen."""
        screen.blit(self.image, (self.rect.x - scroll, self.rect.y))
