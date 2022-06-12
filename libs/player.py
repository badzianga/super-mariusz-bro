# TODO: problem with animation when walking into walls
# TODO: running animation when jumping (extremum)
# TODO: disable constantly jumping when holding jump key
# TODO: player can die when jumping on enemy touching another enemy

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
                'brake': load_image('img/brake_0.png').convert_alpha(),
                'upgrade': [load_image(f'img/upgrade_{i}.png').convert_alpha()
                            for i in range(3)]
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
        self.pipe_sound = Sound('sfx/smb_pipe.wav')
        self.kick_sound = Sound('sfx/smb_kick.wav')

        self.in_air = False
        self.crouching = False

        self.die_timer = 0
        self.is_alive = True

        self.size = 0
        self.upgrade_timer = 0
        self.upgrade_sequence = (0, 1, 0, 1, 0, 1, 2, 0, 1, 2)
        self.upgrade_index = 0
        self.is_upgrading = False

        self.invincible = False
        self.hit_time = 0

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
            self.size += 1
            # TODO: don't change rect size when self.size from 1 to 2
            self.rect.inflate_ip(0, 16)
            self.rect.y -= 8
            self.pos.y -= 8

            self.is_upgrading = True

    def downgrade(self) -> None:
        self.pipe_sound.play()

        self.is_upgrading = True
        self.invincible = True
        self.hit_time = time()

    def remove_invincibility(self) -> None:
        if not self.invincible:
            return

        if time() - self.hit_time >= 4:
            self.invincible = False

            # set full visibility to all states
            self.states[0]['idle'].set_alpha(255)
            self.states[0]['jump'].set_alpha(255)
            self.states[0]['brake'].set_alpha(255)
            for image in self.states[0]['run']:
                image.set_alpha(255)

    def update_animation(self, dt: float) -> None:
        # this one is checked ONLY ONCE just after upgrade() or downgrade()
        # TODO: this might be somewhere else, kinda bad it's checked every frame
        if self.is_upgrading:
            self.image = self.states[0]['idle']
            return
        
        if self.state == 'run':
            self.frame_index += 0.25 * abs(self.speed.x) * dt
            # TODO: maybe here fix with running into walls?
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
        # TODO: player should can kill enemies when invincible
        if self.invincible:
            return

        enemy_collisions = spritecollide(self, enemies, False)

        if enemy_collisions:
            player_bottom = self.rect.bottom

            for enemy in enemy_collisions:
                if not enemy.is_alive:
                    continue

                # whole exception for Koopa which is kinda complicated
                if enemy.type == 'koopa':
                    if enemy.state != 'walk' and not enemy.spinning:
                        self.kick_sound.play()
                        if self.in_air:
                            self.speed.y = -6
                            self.rect.bottom = enemy.rect.top
                        else:
                            if self.speed.x > 0:  # touching left enemy side
                                self.rect.right = enemy.rect.left
                            else:  # touching right enemy side
                                self.rect.left = enemy.rect.right
                            # TODO: there should also be points multiplier
                        self.add_points(400)
                        enemy.spin(self.rect.centerx <= enemy.rect.centerx)
                        return

                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                if enemy_top < player_bottom < enemy_center and self.speed.y >= 0:
                    self.stomp_sound.play()
                    self.speed.y = -6
                    self.rect.bottom = enemy_top
                    self.add_points(100)
                    # TODO: points multiplier from combo
                    enemy.death_state()
                    return  # TODO: for testing
                else:
                    if self.size == 0:
                        self.kill()
                    else:
                        self.downgrade()

    def check_mushroom_collisions(self, mushrooms: Group) -> None:
        mushroom_collisions = spritecollide(self, mushrooms, False)

        if mushroom_collisions:
            for mushroom in mushroom_collisions:
                mushroom.kill()
                self.upgrade()
                self.add_points(1000)

    def downgrade_animation(self) -> None:
        # I really don't want to but I have to, so there goes spaghetti
        if time() - self.upgrade_timer >= 0.1:
            self.upgrade_timer = time()
            self.upgrade_index -= 1

            if self.upgrade_index >= 0:
                self.image = self.states[0]['upgrade'][self.upgrade_sequence[self.upgrade_index]]
            else:
                self.is_upgrading = False

                # change size of Mariusz
                self.size = 0
                self.rect.inflate_ip(0, -16)
                self.rect.y += 8
                self.pos.y += 8

                # after animation set images to half-invisible
                self.states[0]['idle'].set_alpha(128)
                self.states[0]['jump'].set_alpha(128)
                self.states[0]['brake'].set_alpha(128)
                for image in self.states[0]['run']:
                    image.set_alpha(128)

    def upgrade_animation(self) -> None:
        if self.invincible:
            self.downgrade_animation()
            return

        if time() - self.upgrade_timer >= 0.1:
            self.upgrade_timer = time()
            self.upgrade_index += 1

            if self.upgrade_index <= 9:
                self.image = self.states[0]['upgrade'][self.upgrade_sequence[self.upgrade_index]]
            else:
                self.is_upgrading = False

    def die_animation(self, dt: float) -> None:
        if time() - self.die_timer >= 0.4: 
            self.move_vertically(dt)

    def kill(self) -> None:
        music.load('music/smb_mariodie.wav')
        music.play()
        self.change_state('die')
        if self.size > 0:
            self.rect.y += 16  # TODO: this might be bad in the future
            self.pos.y += 16  # TODO: this too
        self.size = 0
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

    def update(self, dt: float, coins: Group, tiles: Group,
               enemies: Group, mushrooms: Group) -> None:
        self.remove_invincibility()

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
