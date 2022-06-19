# TODO: kill fireballs when too far from player

from time import time
from types import FunctionType

from pygame.math import Vector2
from pygame.sprite import Group, Sprite, spritecollide
from pygame.surface import Surface
from pygame.mixer import Sound

from .constants import KOOPA


class Fireball(Sprite):
    def __init__(self, images: tuple, position: tuple, direction: int,
                 add_points: FunctionType) -> None:
        super().__init__()

        self.frame = 0
        self.images = images
        self.image: Surface = self.images[0]
        self.last_time = time()

        self.rect = self.image.get_rect(topleft=position)
        self.pos = Vector2(position)
        self.speed = Vector2(direction * 6, 0)

        self.add_points = add_points

        self.kick_sound = Sound('sfx/smb_kick.wav')

    def move_horizontally(self, dt: float) -> None:
        "Change horizontal position of the fireball."
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
                # TODO: explosion animation
                self.kick_sound.play()
                self.kill()

    def check_vertical_collisions(self, tiles: Group) -> None:
        """Check vertical collisions with map tiles and adjust position."""
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.speed.y > 0:  # touching floor
                    self.rect.bottom = tile.rect.top
                    self.pos.y = self.rect.y
                    self.speed.y = -4  # TODO: maybe change this value
                else:  # touching ceiling
                    # TODO: explosion animation
                    self.kill()
                
                return  # finish looking for collisions

    def check_enemy_collisions(self, enemies: Group) -> None:
        """Check collisions with enemies. Kill enemy when collision occurs."""
        enemy_collisions = spritecollide(self, enemies, False)

        if enemy_collisions:
            enemy = enemy_collisions[0]
            # TODO: explosion animation
            self.kick_sound.play()
            self.kill()

            if enemy.type == KOOPA:  # points from Koopa
                self.add_points(200)
            else:  # points form Goomba
                self.add_points(100)

            enemy_collisions[0].kill_animation(enemy, False)

            return  # fireball kills only one enemy

    def update_animation(self) -> None:
        if time() - self.last_time >= 0.1:
            self.last_time = time()
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
            self.image = self.images[self.frame]

    def update(self, dt: float, tiles: Group, enemies: Group) -> None:
        self.update_animation()

        # change vertical position
        self.move_vertically(dt)
        self.check_vertical_collisions(tiles)

        # change horizontal position
        self.move_horizontally(dt)
        self.check_horizontal_collisions(tiles)

        self.check_enemy_collisions(enemies)

    def draw(self, screen: Surface, scroll: int):
        """Draw sprite onto screen."""
        screen.blit(self.image, (self.rect.x - scroll, self.rect.y))
