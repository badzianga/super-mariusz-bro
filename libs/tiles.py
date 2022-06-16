from time import time
from types import FunctionType

from pygame.image import load as load_image
from pygame.mixer import Sound
from pygame.sprite import Sprite
from pygame.surface import Surface


class Tile(Sprite):
    def __init__(self, image: Surface, position: tuple) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(topleft=position)

        self.bumped = False

    def update(self) -> None:
        return

    def bump(self) -> None:
        return

    def destroy(self) -> None:
        return

    def draw(self, screen: Surface, scroll: int):
        """Draw sprite onto screen."""
        screen.blit(self.image, (self.rect.x - scroll, self.rect.y))

class Brick(Tile):
    def __init__(self, image: Surface, position: tuple,
                 create_debris: FunctionType) -> None:
        super().__init__(image, position)

        self.frame = 0
        self.bump_sound = Sound('sfx/smb_bump.wav')
        self.break_sound = Sound('sfx/smb_breakblock.wav')
        self.bumped = False
        self.last_time = time()

        self.create_debris = create_debris

    def update(self) -> None:
        if self.bumped:
            if time() - self.last_time >= 0.015:
                if self.frame < 5:
                    self.rect.y -= 1
                elif self.frame < 10: 
                    self.rect.y += 1
                else:
                    self.bumped = False
                self.frame += 1
                self.last_time = time()

    def bump(self) -> None:
        if self.bumped:
            return
        self.bump_sound.play()
        self.frame = 0
        self.bumped = True
        # just to make sure it gets updated immediately I'm subtracting 1
        self.last_time = time() - 1

    def destroy(self) -> None:
        self.bumped = True
        self.break_sound.play()
        self.create_debris(self.rect.center)
        self.kill()


class CoinBrick(Brick):
    def __init__(self, image: Surface, position: tuple, plate_image: Surface,
                 create_spinning_coin: FunctionType, add_coin) -> None:
        super().__init__(image, position, None)

        self.coins = 6
        self.add_coin = create_spinning_coin
        self.cant_bump = False
        self.plate_image = plate_image

        self.create_spinning_coin = create_spinning_coin
        self.add_coin = add_coin

    def bump(self) -> None:
        if self.bumped or self.cant_bump:
            return
        self.bump_sound.play()
        self.frame = 0
        self.bumped = True
        # just to make sure it gets updated immediately I'm subtracting 1
        self.last_time = time() - 1
        self.coins -= 1
        self.create_spinning_coin((self.rect.x + 4, self.rect.y - 16))
        self.add_coin()
        if self.coins == 0:
            self.image = self.plate_image
            self.cant_bump = True

    def destroy(self) -> None:
        self.bump()


class QuestionBlock(Sprite):
    def __init__(self, position: tuple, create_spinning_coin: FunctionType,
                 add_coin: FunctionType, add_powerup: FunctionType, theme: str,
                 powerup: bool=False) -> None:
        super().__init__()

        self.images = [
            load_image(f'img/question_block_{i}.png').convert_alpha()
            for i in range(3)
        ]
        self.images.append(load_image(f'img/{theme}/plate_0.png').convert_alpha())
        self.frame = 0
        self.animation = ((0, 0.45), (1, 0.15), (2, 0.15), (1, 0.15))
        self.last_time = time()

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=position)

        self.bump_sound = Sound('sfx/smb_bump.wav')
        self.powerup_sound = Sound('sfx/smb_powerup_appears.wav')

        self.updated = False
        self.powerup = powerup
        self.bumped = False
        self.created_coin = False
        self.played_powerup_sound = False

        self.create_spinning_coin = create_spinning_coin
        self.add_coin = add_coin
        self.add_powerup = add_powerup

    def update(self) -> None:
        if self.updated:
            return
        if self.bumped:
            if self.powerup:
                if not self.played_powerup_sound:
                    self.powerup_sound.play()
                    self.played_powerup_sound = True
            else:
                if not self.created_coin:
                    self.create_spinning_coin((self.rect.x + 4, self.rect.y - 16))
                    self.add_coin()
                    self.created_coin = True
            if time() - self.last_time >= 0.015:
                if self.frame < 5:
                    self.rect.y -= 1
                elif self.frame < 10: 
                    self.rect.y += 1
                else:
                    self.updated = True
                    if self.powerup:
                        # TODO: juhuuu
                        self.add_powerup((self.rect.x, self.rect.y - 16))
                self.frame += 1
                self.last_time = time()
            
        elif time() - self.last_time >= self.animation[self.frame][1]:
            self.last_time = time()
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0
            self.image = self.images[self.animation[self.frame][0]]

    def bump(self) -> None:
        if self.bumped:
            return
        self.bump_sound.play()
        self.image = self.images[3]
        self.bumped = True
        self.frame = 0
        # just to make sure it gets updated immediately I'm subtracting 1
        self.last_time = time() - 1

    def destroy(self) -> None:
        # it can't be destroyed, but this function must exist
        self.bump()

    def draw(self, screen: Surface, scroll: int):
        """Draw sprite onto screen."""
        screen.blit(self.image, (self.rect.x - scroll, self.rect.y))


class Decoration(Sprite):
    def __init__(self, position: tuple, image: Surface) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen: Surface, scroll: int) -> None:
        screen.blit(self.image, (self.rect.x - scroll, self.rect.y))
