from types import FunctionType

from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_x, K_z
from pygame.image import load as load_image
from pygame.key import get_pressed
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from pygame.transform import flip


class Mariusz(Sprite):
    def __init__(self, screen: Surface, x: int, y: int,
                 add_coin: FunctionType, reset_coins: FunctionType) -> None:
        super().__init__()

        self.screen = screen

        self.state = 'idle'
        self.frame_index = 0
        self.states = {
            'idle': load_image('img/idle_0.png').convert_alpha(),
            'run': [load_image(f'img/run_{i}.png').convert_alpha()
                    for i in range(3)],
            'jump': load_image('img/jump_0.png').convert_alpha(),
            'die': load_image('img/die_0.png').convert_alpha(),
            'brake': load_image('img/brake_0.png').convert_alpha()
        }
        self.image = self.states['idle']
        self.flip = False

        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = Vector2(x, y)
        self.speed = Vector2(0, 0)

        self.add_coin = add_coin
        self.reset_coins = reset_coins

        self.coin_sound = Sound('sfx/smb_coin.wav')
        self.oneup_sound = Sound('sfx/smb_1-up.wav')
        self.jump_sound = Sound('sfx/smb_jump-small.wav')

        self.in_air = False

    def change_state(self, new_state: str) -> None:
        if new_state != self.state:
            self.state = new_state
            self.frame_index = 0

    def update_animation(self, dt: float) -> None:
        if self.state == "run":
            self.frame_index += 0.25 * abs(self.speed.x) * dt
            if self.frame_index >= 3:
                self.frame_index = 0
            self.image = self.states[self.state][int(self.frame_index)]
        else:
            self.image = self.states[self.state]

    def move_horizontally(self, dt: float) -> None:
        keys = get_pressed()

        if keys[K_LEFT]:
            if self.speed.x > 0:
                self.change_state("brake")
            else:
                self.change_state("run")
            self.speed.x = max(self.speed.x - 0.2 * dt, -2)
            self.flip = True
        if keys[K_RIGHT]:
            if self.speed.x < 0:
                self.change_state("brake")
            else:
                self.change_state("run")
            self.speed.x = min(self.speed.x + 0.2 * dt, 2)
            self.flip = False

        if ((keys[K_LEFT] and keys[K_RIGHT]) or
            (not keys[K_LEFT] and not keys[K_RIGHT])):
            if self.speed.x > 0.2:
                self.speed.x -= 0.075 * dt
            elif self.speed.x < -0.2:
                self.speed.x += 0.075 * dt
            else:
                self.speed.x = 0
                self.change_state("idle")
        self.pos.x += self.speed.x * dt
        self.rect.x = self.pos.x

    def move_vertically(self, dt: float) -> None:
        self.speed.y = min(self.speed.y + 1 * dt, 8)

        if not self.in_air:
            keys = get_pressed()
            if keys[K_z]:  # jump
                self.jump_sound.play()
                self.speed.y = -8
                self.in_air = True

        self.pos.y += self.speed.y * dt
        self.rect.y = self.pos.y

    def check_horizontal_collisions(self, tiles: Group) -> None:
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                # touching right wall
                if self.speed.x < 0:
                    self.rect.left = tile.rect.right
                    self.pos.x = self.rect.x
                    self.speed.x = 0
                    return  # finish looking for collisions
                # touching left wall
                elif self.speed.x > 0:
                    self.rect.right = tile.rect.left
                    self.pos.x = self.rect.x
                    self.speed.x = 0
                    return  # finish looking for collisions

    def check_vertical_collisions(self, tiles: Group) -> None:
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                # touching floor
                if self.speed.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.pos.y = self.rect.y
                    self.speed.y = 0
                    self.in_air = False
                return  # finish looking for collisions
        print(self.speed.y)
        if abs(self.speed.y) > 1.5:
            self.in_air = True
            self.change_state("jump")

    def check_coin_collision(self, coins: Group) -> None:
        for coin in coins:
            if self.rect.colliderect(coin.rect):
                coin.kill()
                if self.add_coin() >= 100:
                    self.reset_coins()
                    self.oneup_sound.play()
                else:
                    self.coin_sound.play()

    def draw(self) -> None:
        if self.flip:
            self.screen.blit(flip(self.image, True, False), self.rect)
        else:
            self.screen.blit(self.image, self.rect)

    def update(self, dt: float, coins: Group, tiles: Group) -> None:
        self.move_horizontally(dt)
        self.check_horizontal_collisions(tiles)

        self.move_vertically(dt)
        self.check_vertical_collisions(tiles)

        self.check_coin_collision(coins)

        self.update_animation(dt)

        self.draw()
