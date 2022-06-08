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

    def update(self) -> None:
        pass

    def bump(self) -> None:
        return


class Brick(Tile):
    def __init__(self, image: Surface, position: tuple) -> None:
        super().__init__(image, position)

        self.frame = 0
        self.sound = Sound('sfx/smb_bump.wav')
        self.bumped = False
        self.last_time = time()

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
        self.sound.play()
        self.frame = 0
        self.bumped = True
        # just to make sure it gets updated immediately I'm subtracting 1
        self.last_time = time() - 1


class QuestionBlock(Sprite):
    def __init__(self, position: tuple, create_spinning_coin: FunctionType,
                 add_coin: FunctionType, powerup: bool=False) -> None:
        super().__init__()

        self.images = [
            load_image(f'img/question_block_{i}.png').convert_alpha()
            for i in range(3)
        ]
        self.images.append(load_image('img/plate_0.png').convert_alpha())
        self.frame = 0
        self.animation = ((0, 0.45), (1, 0.15), (2, 0.15), (1, 0.15))
        self.last_time = time()

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=position)

        self.sound = Sound('sfx/smb_bump.wav')
        self.bumped = False
        self.powerup = powerup
        self.just_bumped = False
        self.created_coin = False

        self.create_spinning_coin = create_spinning_coin
        self.add_coin = add_coin

    def update(self) -> None:
        if self.bumped:
            return
        if self.just_bumped:
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
                    self.bumped = True
                self.frame += 1
                self.last_time = time()
            
        elif time() - self.last_time >= self.animation[self.frame][1]:
            self.last_time = time()
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0
            self.image = self.images[self.animation[self.frame][0]]

    def bump(self) -> None:
        self.sound.play()
        self.image = self.images[3]
        self.just_bumped = True
        self.frame = 0
        # just to make sure it gets updated immediately I'm subtracting 1
        self.last_time = time() - 1
