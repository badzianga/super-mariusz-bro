from pygame.sprite import Sprite, Group
from pygame.math import Vector2
from pygame.surface import Surface


class Mushroom(Sprite):
    def __init__(self, image: Surface, position: tuple) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.pos = Vector2(position)
        self.speed = Vector2(1.5, 0)

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
        self.move_horizontally(dt)
        self.check_horizontal_collisions(tiles)

        self.move_vertically(dt)
        self.check_vertical_collisions(tiles)


class OneUP(Mushroom):
    def __init__(self, image: Surface, position: tuple) -> None:
        super().__init__(image, position)


class Star(Sprite):
    def __init__(self, image: Surface, position: tuple) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(topleft=position)


class FireFlower(Sprite):
    def __init__(self, image: Surface, position: tuple) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(topleft=position)
