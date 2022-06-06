from time import time

from pygame.image import load as load_image
from pygame.sprite import Sprite
from pygame.surface import Surface


class Coin(Sprite):
    """Animated static Coin object visible on map."""

    def __init__(self, position: tuple, theme: str) -> None:
        """Initialize Coin object."""
        super().__init__()

        # animation and visual stuff
        self.images = [
            load_image(f'img/{theme}/coin_{i}.png').convert_alpha()
            for i in range(3)
        ]
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
