# TODO: fix Koopa points

from time import time

from pygame.image import load as load_image
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from pygame.transform import flip as flip_image

from .constants import GOOMBA, KOOPA


class Goomba(Sprite):
    """
    First and most basic enemy. It can walk and collide with map and enemies.
    """

    def __init__(self, x: int, y: int, theme: str) -> None:
        """Initialize enemy - Goomba."""
        super().__init__()

        self.is_alive = True  # used in updating and player's collision check
        self.type = GOOMBA

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

        # TODO: maybe change method of killing enemies with spinning Koopa
        # to be honest, it's only used in Koopa, but it's easier to add it here
        self.spinning = False
        # sound when killing other enemies - also Koopa exclusive
        self.kick_sound = Sound('sfx/smb_kick.wav')

        # positioning and movement stuff
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = Vector2(x, y)
        self.speed = Vector2(-1, 0)

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

    def check_enemy_collisions(self, enemies: Group) -> None:
        """Check collisions with other enemies."""
        for enemy in enemies:
            if self == enemy:
                continue

            if self.rect.colliderect(enemy.rect):
                if enemy.type == KOOPA and enemy.spinning:
                    # TODO: death animation, add points
                    enemy.kick_sound.play()
                    self.kill()
                    return
                elif self.type == KOOPA and self.spinning:
                    # TODO: death animation, add points
                    self.kick_sound.play()
                    enemy.kill()
                    return
                        
                if self.speed.x > 0:  # touching left side of the other enemy
                    self.rect.right = enemy.rect.left
                    self.pos.x = self.rect.x
                else:  # touching right side of the other enemy
                    self.rect.left = enemy.rect.right
                    self.pos.x = self.rect.x
                self.speed *= -1
                enemy.speed *= -1

    def death_state(self) -> None:
        """Change alive state of the enemy to false and make it squished."""
        self.last_time = time()
        self.image = self.images['die']
        self.is_alive = False

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(self, dt: float, tiles: Group, enemies: Group) -> None:
        """Update enemy image and position, disappear it after squished."""
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

        self.check_enemy_collisions(enemies)


class Koopa(Goomba):
    """
    Second basic enemy. It can walk, collde with map and enemies and kill other
    enemies when jumped on again.
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialize enemy - Koopa."""
        super().__init__(x, y, 'red')

        # only differences from Goomba
        self.type = KOOPA
        self.spinning = False
        self.state = 'walk'
        self.images = {
            'walk': [
                load_image(f'img/koopa_walk_{i}.png').convert_alpha()
                for i in range(2)
            ],
            'die': load_image('img/koopa_die_0.png').convert_alpha(),
            'reviving': load_image('img/koopa_reviving_0.png').convert_alpha()
        }
        self.flip = False
        self.image = self.images['walk'][0]
        # I'm not overriding self.rect because I want 16x16, not 16x24

    def death_state(self) -> None:
        self.image = self.images['die']
        self.state = 'die'
        self.last_time = time()

    def spin(self, to_right: bool) -> None:
        self.spinning = True
        self.speed.x = 6 if to_right else -6
        # just to be sure, why not
        self.state = 'die'
        self.image = self.images['die'] 

    def stop_spinning(self) -> None:
        self.spinning = False
        self.speed.x = self.speed.x // 6
        self.last_time = time()

    def draw(self, screen: Surface) -> None:
        if self.state == 'walk':
            screen.blit(flip_image(self.image, self.flip, False),
                        (self.rect.x, self.rect.y - 8))
        else:
            screen.blit(flip_image(self.image, self.flip, False),
                        (self.rect.x, self.rect.y))

    def update(self, dt: float, tiles: Group, enemies: Group) -> None:
        """Update enemy image and position."""
        if self.state == 'walk':  # alive state - update walking image
            if time() - self.last_time >= self.animation_speed:
                self.last_time = time()
                self.frame += 1
                if self.frame >= 2:
                    self.frame = 0
            self.image = self.images['walk'][self.frame]
        elif not self.spinning:  # died or reviving
            time_diff = time() - self.last_time
            if time_diff >= 5:
                self.state = 'walk'
                self.image = self.images['walk'][self.frame]
                self.last_time = time()
            elif time_diff >= 4:
                self.state = 'reviving'
                self.image = self.images['reviving']

        if self.state == 'walk' or self.spinning:
            # change horizontal position
            self.move_horizontally(dt)
            self.check_horizontal_collisions(tiles)

            # change vertical position
            self.move_vertically(dt)
            self.check_vertical_collisions(tiles)

            self.check_enemy_collisions(enemies)

            self.flip = self.speed.x > 0
