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

    def bump(self) -> None:
        return


class QuestionBlock(Sprite):
    def __init__(self, position: tuple, powerup: bool=False) -> None:
        super().__init__()

        self.images = [
            load_image(f'img/question_block_{i}.png').convert_alpha()
            for i in range(3)
        ]
        self.frame = 0
        self.animation = ((0, 0.45), (1, 0.15), (2, 0.15), (1, 0.15))
        self.last_time = time()

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=position)

        self.sound = Sound('sfx/smb_bump.wav')

    def update(self) -> None:
        if time() - self.last_time >= self.animation[self.frame][1]:
            self.last_time = time()
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0
        self.image = self.images[self.animation[self.frame][0]]

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def bump(self) -> None:
        self.sound.play()
