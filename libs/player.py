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

        self.image = load_image("img/idle_0.png").convert_alpha()
        self.flip = False

        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = Vector2(x, y)
        self.speed = Vector2(0, 0)

        self.add_coin = add_coin
        self.reset_coins = reset_coins
        self.coin_sound = Sound('sfx/smb_coin.wav')
        self.oneup_sound = Sound('sfx/smb_1-up.wav')

    def move_horizontally(self, dt: float) -> None:
        keys = get_pressed()

        if keys[K_LEFT]:
            self.speed.x = max(self.speed.x - 0.2 * dt, -2)
            self.flip = True
        if keys[K_RIGHT]:
            self.speed.x = min(self.speed.x + 0.2 * dt, 2)
            self.flip = False

        if not keys[K_LEFT] and not keys[K_RIGHT]:
            if self.speed.x > 0.2:
                self.speed.x -= 0.1 * dt
            elif self.speed.x < -0.2:
                self.speed.x += 0.1 * dt
            else:
                self.speed.x = 0
        self.pos.x += self.speed.x * dt
        self.rect.x = self.pos.x

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

    def update(self, dt: float, coins: Group) -> None:
        self.move_horizontally(dt)
        self.check_coin_collision(coins)

        self.draw()
