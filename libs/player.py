# TODO: problem with animation when walking into walls
# TODO: running animation when jumping (extremum)
# TODO: disable constantly jumping when holding jump key

from time import time
from types import FunctionType

from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_a, K_z
from pygame.image import load as load_image
from pygame.key import get_pressed
from pygame.math import Vector2
from pygame.mixer import Sound, music
from pygame.sprite import Group, Sprite, spritecollide
from pygame.surface import Surface
from pygame.transform import flip
from pygame import draw

from libs.constants import WHITE


class Mariusz(Sprite):
    def __init__(self, screen: Surface, position: tuple, size: int,
                 add_coin: FunctionType, add_points: FunctionType) -> None:
        super().__init__()

        self.screen = screen

        self.size = size

        self.state = 'idle'
        self.frame_index = 0
        self.states = {
            0: {
                'idle': load_image('img/idle_0.png').convert_alpha(),
                'run': [load_image(f'img/run_{i}.png').convert_alpha()
                        for i in range(3)],
                'jump': load_image('img/jump_0.png').convert_alpha(),
                'die': load_image('img/die_0.png').convert_alpha(),
                'brake': load_image('img/brake_0.png').convert_alpha()
            },
            1: {
                'idle': load_image('img/large_idle_0.png').convert_alpha(),
                'run': [load_image(f'img/large_run_{i}.png').convert_alpha()
                        for i in range(3)],
                'jump': load_image('img/large_jump_0.png').convert_alpha(),
                'crouch': load_image('img/large_crouch_0.png').convert_alpha(),
                'brake': load_image('img/large_brake_0.png').convert_alpha()
            }
        }
        self.image = self.states[self.size]['idle']
        self.flip = False

        self.rect = self.image.get_rect(topleft=position)
        self.pos = Vector2(position)
        self.speed = Vector2(0, 0)

        self.add_coin = add_coin
        self.add_points = add_points

        self.jump_sound = Sound('sfx/smb_jump-small.wav')
        self.large_jump_sound = Sound('sfx/smb_jump-super.wav')
        self.stomp_sound = Sound('sfx/smb_stomp.wav')
        self.powerup_sound = Sound('sfx/smb_powerup.wav')

        self.in_air = False
        self.crouching = False

        self.die_timer = 0
        self.is_alive = True

        self.size = 0
        self.upgrade_timer = 0
        self.upgrade_sequence = (1, 2, 1, 2, 1, 2, 3, 1, 2, 3)
        self.upgrade_index = 0
        self.is_upgrading = False

    def change_state(self, new_state: str) -> None:
        if new_state != self.state:
            self.state = new_state
            self.frame_index = 0

    def run_from_jump(self) -> None:
        if self.state == 'jump':
            self.state = 'run'
            self.frame_index = 0

    def upgrade(self) -> None:
        self.powerup_sound.play()
        if self.size != 2:
            self.speed.y = 0  # TODO: it could be only temporary
            self.size += 1
            # TODO: don't change rect size when self.size from 1 to 2
            self.rect.inflate_ip(0, 16)
            self.rect.y -= 8
            self.pos.y -= 8
            
            self.is_upgrading = True

    def update_animation(self, dt: float) -> None:
        if self.state == 'run':
            self.frame_index += 0.25 * abs(self.speed.x) * dt
            if self.frame_index >= 3:
                self.frame_index = 0
            self.image = self.states[self.size][self.state][int(self.frame_index)]
        else:
            self.image = self.states[self.size][self.state]

    def move_horizontally(self, dt: float) -> None:
        keys = get_pressed()

        if keys[K_a]:
            max_speed = 4
            brake_speed = 0.3
        else:
            max_speed = 2
            brake_speed = 0.2

        if keys[K_DOWN] and not self.in_air:
            if self.size > 0:
                self.change_state('crouch')
            self.crouching = True
        else:
            self.crouching = False

        if keys[K_LEFT] and not self.crouching:
            if self.speed.x > 0:
                self.change_state('brake')
                self.speed.x = max(self.speed.x - brake_speed * dt, -max_speed)
            else:
                self.change_state('run')
                self.speed.x = max(self.speed.x - 0.2 * dt, -max_speed)
            self.flip = True
        if keys[K_RIGHT] and not self.crouching:
            if self.speed.x < 0:
                self.change_state('brake')
                self.speed.x = min(self.speed.x + brake_speed * dt, max_speed)
            else:
                self.change_state('run')
                self.speed.x = min(self.speed.x + 0.2 * dt, max_speed)
            self.flip = False

        if not self.in_air:
            if ((keys[K_LEFT] and keys[K_RIGHT]) or
                (not keys[K_LEFT] and not keys[K_RIGHT]) or
                self.crouching):
                if self.speed.x > 0.2:
                    if self.crouching:
                        self.speed.x -= 0.15 * dt
                    else:
                        self.speed.x -= 0.075 * dt
                    self.run_from_jump()
                elif self.speed.x < -0.2:
                    if self.crouching:
                        self.speed.x += 0.15 * dt
                    else:
                        self.speed.x += 0.075 * dt
                    self.run_from_jump()
                else:
                    self.speed.x = 0
                    if not self.crouching or (self.crouching and self.size == 0):
                        self.change_state('idle')

        self.pos.x += self.speed.x * dt
        self.rect.x = self.pos.x

    def move_vertically(self, dt: float) -> None:
        self.speed.y = min(self.speed.y + 1 * dt, 8)

        if not self.in_air:
            keys = get_pressed()
            if keys[K_z]:  # jump
                if self.size == 0:
                    self.jump_sound.play()
                else:
                    self.large_jump_sound.play()
                self.speed.y = -8
                self.in_air = True

        self.pos.y += self.speed.y * dt
        self.rect.y = self.pos.y

    def check_horizontal_collisions(self, tiles: Group) -> None:
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
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
            if self.rect.colliderect(tile.rect):
                # touching floor
                if self.speed.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.pos.y = self.rect.y
                    self.speed.y = 0
                    self.in_air = False
                elif self.speed.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.pos.y = self.rect.y
                    self.speed.y = 0
                    # TODO: destroying tile wouldn't kill enemy
                    if self.size == 0:
                        tile.bump()
                    else:
                        tile.destroy()
                return  # finish looking for collisions
        if abs(self.speed.y) > 1.5:
            self.in_air = True
            self.change_state('jump')

    def check_coin_collision(self, coins: Group) -> None:
        coin_collisions = spritecollide(self, coins, False)

        for coin in coin_collisions:
            coin.kill()
            self.add_coin()

    def check_enemy_collisions(self, enemies: Group) -> None:
        enemy_collisions = spritecollide(self, enemies, False)

        if enemy_collisions:
            player_bottom = self.rect.bottom

            for enemy in enemy_collisions:
                if not enemy.is_alive:
                    continue

                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                if enemy_top < player_bottom < enemy_center and self.speed.y >= 0:
                    self.stomp_sound.play()
                    self.speed.y = -6
                    self.add_points(100)
                    # TODO: points multiplier from combo
                    enemy.death_state()
                else:
                    if self.size == 0:
                        self.kill()
                    else:
                        # TODO: shrinking animation and invincibility
                        self.size = 0
                        self.rect.inflate_ip(0, -16)
                        self.rect.y += 8
                        self.pos.y += 8

    def check_mushroom_collisions(self, mushrooms: Group) -> None:
        mushroom_collisions = spritecollide(self, mushrooms, False)

        if mushroom_collisions:
            for mushroom in mushroom_collisions:
                mushroom.kill()
                self.upgrade()
                self.add_points(1000)

    def upgrade_animation(self) -> None:
        if time() - self.upgrade_timer >= 0.1:
            self.upgrade_timer = time()
            self.upgrade_index += 1
            if self.upgrade_index >= 10:
                self.upgrade_index = 0
                self.is_upgrading = False
                return

    def die_animation(self, dt: float) -> None:
        if time() - self.die_timer >= 0.4: 
            self.move_vertically(dt)

    def kill(self) -> None:
        music.load('music/smb_mariodie.wav')
        music.play()
        self.change_state('die')
        self.image = self.states[self.size]['die']
        self.is_alive = False
        self.speed.x = 0
        self.speed.y = -10
        self.die_timer = time()

    def draw(self) -> None:
        if self.flip:
            self.screen.blit(flip(self.image, True, False), self.rect)
        else:
            self.screen.blit(self.image, self.rect)
        draw.rect(self.screen, WHITE, self.rect, 1)

    def update(self, dt: float, coins: Group, tiles: Group,
               enemies: Group, mushrooms: Group) -> None:
        self.move_horizontally(dt)
        self.check_horizontal_collisions(tiles)

        self.move_vertically(dt)
        self.check_vertical_collisions(tiles)

        self.check_coin_collision(coins)

        self.check_enemy_collisions(enemies)

        # TODO: there is a bug when jumping immediately after upgrade sequence
        # if it will be even after changes in jumping mechanics
        # move this function before move_horizontally() 
        self.check_mushroom_collisions(mushrooms)

        self.update_animation(dt)
