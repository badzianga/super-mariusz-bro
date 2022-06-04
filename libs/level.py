# TODO: Add coins to level and remove them from the controller

from pygame.image import load as load_image
from pygame.sprite import Group
from pygame.surface import Surface

from .tiles import Brick, QuestionBlock, Tile

level_0 = [  # temporary map - for testing only
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 3, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Level:
    def __init__(self, screen: Surface) -> None:
        self.tiles = Group()
        self.tile_img = load_image('img/rock_0.png').convert()
        self.brick_img = load_image('img/brick_0.png').convert()

        self.screen = screen

        self.load_level()

    def load_level(self) -> None:
        for y, row in enumerate(level_0):
            for x, cell in enumerate(row):
                if cell == 0:
                    continue
                elif cell == 1:
                    self.tiles.add(Tile(self.tile_img, (x * 16, y * 16 + 8)))
                elif cell == 2:
                    self.tiles.add(QuestionBlock((x * 16, y * 16 + 8)))
                elif cell == 3:
                    self.tiles.add(Brick(self.brick_img, (x * 16, y * 16 + 8)))

    def draw(self) -> None:
        self.tiles.draw(self.screen)
