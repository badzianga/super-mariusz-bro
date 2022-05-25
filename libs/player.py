from pygame.image import load as load_image
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface


class Mariusz(Sprite):
    def __init__(self, screen: Surface, x: int, y: int) -> None:
        super().__init__()

        self.screen = screen

        self.image = load_image("img/idle_0.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = Vector2(x, y)

    def draw(self):
        self.screen.blit(self.image, self.rect)
