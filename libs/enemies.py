# TODO: enemy should collide with other enemies
# TODO: Mario shouldn't die when jumping on two overlapping enemies

from time import time

from pygame.image import load as load_image
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from pygame.surface import Surface


class Goomba(Sprite):
    def __init__(self, x: int, y: int, theme: str) -> None:
        super().__init__()

        self.state = 'walk'
        self.frame = 0
        self.states = {
            'walk': [
                load_image(f'img/{theme}/goomba_walk_{i}.png').convert_alpha()
                for i in range(2)
            ],
            'die': load_image(f'img/{theme}/goomba_die_0.png').convert_alpha()
        }
        self.animation_speed = 0.3
        self.last_time = time()
        self.image = self.states['walk'][0]

        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = Vector2(x, y)
        self.speed = Vector2(1, 0)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def move_horizontally(self, dt: float) -> None:
        self.pos.x += self.speed.x * dt
        self.rect.x = self.pos.x

    def move_vertically(self, dt: float) -> None:
        self.speed.y = min(self.speed.y + 1 * dt, 8)

        self.pos.y += self.speed.y * dt
        self.rect.y = self.pos.y

    def check_horizontal_collisions(self, tiles: Group) -> None:
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                # touching right wall
                if self.speed.x < 0:
                    self.rect.left = tile.rect.right
                    self.pos.x = self.rect.x
                    self.speed.x *= -1
                    return  # finish looking for collisions
                # touching left wall
                elif self.speed.x > 0:
                    self.rect.right = tile.rect.left
                    self.pos.x = self.rect.x
                    self.speed.x *= -1
                    return  # finish looking for collisions

    def check_vertical_collisions(self, tiles: Group) -> None:
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                # touching floor
                if self.speed.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.pos.y = self.rect.y
                    self.speed.y = 0
                return  # finish looking for collisions

    def update(self, dt: float, tiles: Group) -> None:
        if self.state == 'walk':
            if time() - self.last_time >= self.animation_speed:
                self.last_time = time()
                self.frame += 1
                if self.frame >= 2:
                    self.frame = 0
            self.image = self.states['walk'][self.frame]

        self.move_horizontally(dt)
        self.check_horizontal_collisions(tiles)

        self.move_vertically(dt)
        self.check_vertical_collisions(tiles)
