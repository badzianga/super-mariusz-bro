from pygame.image import load as load_image
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.key import get_pressed
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_z, K_x


class Mariusz(Sprite):
    def __init__(self, screen: Surface, x: int, y: int) -> None:
        super().__init__()

        self.screen = screen

        self.image = load_image("img/idle_0.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = Vector2(x, y)
        self.speed = Vector2(0, 0)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self, dt: float):
        keys = get_pressed()

        if keys[K_LEFT]:
            self.speed.x = max(self.speed.x - 0.1 * dt, -2)
        if keys[K_RIGHT]:
            self.speed.x = min(self.speed.x + 0.1 * dt, 2)
        if not keys[K_LEFT] and not keys[K_RIGHT]:
            if self.speed.x > 0.2:
                self.speed.x -= 0.1 * dt
            elif self.speed.x < -0.2:
                self.speed.x += 0.1 * dt
            else:
                self.speed.x = 0
        self.pos.x += self.speed.x * dt
        self.rect.x = self.pos.x

        self.draw()
