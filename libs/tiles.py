from time import time

from pygame.image import load as load_image
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.mixer import Sound


class Tile(Sprite):
    def __init__(self, image: Surface, position: tuple) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(topleft=position)

    def update(self) -> None:
        pass

    def bump(self) -> None:
        return


class QuestionBlock(Sprite):
    def __init__(self, position: tuple, powerup: bool=False) -> None:
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
        self.just_bumped = False

    def update(self) -> None:
        if self.bumped:
            return
        if self.just_bumped:
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

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def bump(self) -> None:
        self.sound.play()
        self.image = self.images[3]
        self.just_bumped = True
        self.frame = 0
