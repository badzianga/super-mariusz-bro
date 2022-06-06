# TODO: enemy should collide with other enemies
# TODO: Mario shouldn't die when jumping on two overlapping enemies

from time import time

from pygame.image import load as load_image
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from pygame.surface import Surface


class Goomba(Sprite):
    """First and most basic enemy. It can walk and collide with map."""

    def __init__(self, x: int, y: int, theme: str) -> None:
        """Initialize enemy - Goomba."""
        super().__init__()

        self.is_alive = True  # used in updating and player's collision check

        # animations and visual stuff
        self.frame = 0
        self.images = {
            'walk': [
                load_image(f'img/{theme}/goomba_walk_{i}.png').convert_alpha()
                for i in range(2)
            ],
            'die': load_image(f'img/{theme}/goomba_die_0.png').convert_alpha()
        }
        self.animation_speed = 0.3
        self.last_time = time()
        self.image = self.images['walk'][0]

        # positioning and movement stuff
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = Vector2(x, y)
        self.speed = Vector2(1, 0)

    def draw(self, screen: Surface) -> None:
        """Draw enemy onto screen."""
        screen.blit(self.image, self.rect)

    def move_horizontally(self, dt: float) -> None:
        "Change horizontal position of the enemy."
        self.pos.x += self.speed.x * dt
        self.rect.x = self.pos.x

    def move_vertically(self, dt: float) -> None:
        "Apply gravity and change vertical position of the enemy."
        self.speed.y = min(self.speed.y + 1 * dt, 8)

        self.pos.y += self.speed.y * dt
        self.rect.y = self.pos.y

    def check_horizontal_collisions(self, tiles: Group) -> None:
        """Check horizontal collisions with map tiles and adjust position."""
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.speed.x < 0:  # touching right wall
                    self.rect.left = tile.rect.right
                    self.pos.x = self.rect.x
                    self.speed.x *= -1
                    return  # finish looking for collisions

                elif self.speed.x > 0:  # touching left wall
                    self.rect.right = tile.rect.left
                    self.pos.x = self.rect.x
                    self.speed.x *= -1
                    return  # finish looking for collisions

    def check_vertical_collisions(self, tiles: Group) -> None:
        """Check vertical collisions with map tiles and adjust position."""
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.speed.y > 0:  # touching floor
                    # TODO: kill enemy if tile.bumped
                    self.rect.bottom = tile.rect.top
                    self.pos.y = self.rect.y
                    self.speed.y = 0
                return  # finish looking for collisions

    def death_state(self) -> None:
        """Change alive state of the enemy to false and make it squished."""
        # self.frame = 0  # isn't really necessary
        self.last_time = time()
        self.image = self.images['die']
        self.is_alive = False

    def update(self, dt: float, tiles: Group) -> None:
        """Update enemy image, and position, disappear it after squished."""
        if self.is_alive:  # alive state - update walking image
            if time() - self.last_time >= self.animation_speed:
                self.last_time = time()
                self.frame += 1
                if self.frame >= 2:
                    self.frame = 0
            self.image = self.images['walk'][self.frame]
        else:  # die state
            if time() - self.last_time >= 0.4:
                self.kill()
            return

        # change horizontal position
        self.move_horizontally(dt)
        self.check_horizontal_collisions(tiles)

        # change vertical position
        self.move_vertically(dt)
        self.check_vertical_collisions(tiles)
