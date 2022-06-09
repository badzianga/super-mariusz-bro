# TODO: add coins to level and remove them from the controller
# TODO: load map data from files
# TODO: match-case instead of if statements

from types import FunctionType
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
    [1, 0, 0, 3, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Level:
    """Object with map data that contains all tiles."""

    def __init__(self, screen: Surface) -> None:
        self.screen = screen

        self.tiles = Group()

        # temporary, these will be in Controller in the future
        self.tile_img = load_image('img/rock_0.png').convert()
        self.brick_img = load_image('img/brick_0.png').convert()

    def load_level(self, create_spinning_coin: FunctionType,
                   add_coin: FunctionType, create_debris: FunctionType,
                   add_powerup: FunctionType) -> None:
        """Load tiles and add them to the tiles group."""
        for y, row in enumerate(level_0):
            for x, cell in enumerate(row):
                if cell == 0:
                    continue
                elif cell == 1:
                    self.tiles.add(Tile(self.tile_img, (x * 16, y * 16 + 8)))
                elif cell == 2:
                    self.tiles.add(
                        QuestionBlock((x * 16, y * 16 + 8), create_spinning_coin,
                                      add_coin, add_powerup, True)
                        )
                elif cell == 3:
                    self.tiles.add(Brick(self.brick_img, (x * 16, y * 16 + 8),
                                         create_debris))

    def draw(self) -> None:
        """Draw all tiles onto screen."""
        self.tiles.draw(self.screen)
