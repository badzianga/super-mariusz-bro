from types import FunctionType

from numpy import loadtxt, uint8
from pygame.image import load as load_image
from pygame.sprite import Group
from pygame.surface import Surface

from .coin import Coin
from .enemies import Goomba, Koopa
from .tiles import Brick, Decoration, QuestionBlock, Tile


class Level:
    """Object with map data that contains all tiles."""

    def __init__(self, screen: Surface, world: str) -> None:
        self.screen = screen

        self.tiles = Group()
        self.coins = Group()
        self.enemies = Group()
        self.decorations = Group()

        # temporary, these will be in Controller in the future
        self.rock_img = load_image('img/rock_0.png').convert()
        self.block_img = load_image('img/block_0.png').convert()
        self.brick_img_0 = load_image('img/brick_0.png').convert()
        self.brick_img_1 = load_image('img/brick_1.png').convert()
        self.plate_img = load_image('img/plate_0.png').convert()
        self.hill_img_0 = load_image('img/hill_0.png').convert_alpha()
        self.hill_img_1 = load_image('img/hill_1.png').convert_alpha()
        self.bush_img_0 = load_image('img/bush_0.png').convert_alpha()
        self.bush_img_1 = load_image('img/bush_1.png').convert_alpha()
        self.bush_img_2 = load_image('img/bush_2.png').convert_alpha()
        self.cloud_img_0 = load_image('img/cloud_0.png').convert_alpha()
        self.cloud_img_1 = load_image('img/cloud_1.png').convert_alpha()
        self.cloud_img_2 = load_image('img/cloud_2.png').convert_alpha()
        self.pipe_img_0 = load_image('img/pipe_0.png').convert_alpha()
        self.pipe_img_1 = load_image('img/pipe_1.png').convert_alpha()

        # TODO: temporary?
        self.world = world

    def load_level(self, create_spinning_coin: FunctionType,
                   add_coin: FunctionType, create_debris: FunctionType,
                   add_powerup: FunctionType) -> tuple:
        """Load level from file. Returns player position."""
    
        world_data = loadtxt(f"maps/world_{self.world}.csv",
                             dtype=uint8, delimiter=',')
    
        for y, row in enumerate(world_data):
            for x, cell in enumerate(row):
                match cell:
                    case 0:
                        continue
                    case 1:  # rock
                        self.tiles.add(
                            Tile(self.rock_img, (x * 16, y * 16 + 8))
                        )
                    case 2:  # block
                        self.tiles.add(
                            Tile(self.block_img, (x * 16, y * 16 + 8))
                        )
                    case 3:  # brick_0
                        self.tiles.add(
                            Brick(self.brick_img_0, (x * 16, y * 16 + 8),
                                  create_debris)
                        )
                    case 4:  # brick_1
                        self.tiles.add(
                            Brick(self.brick_img_0, (x * 16, y * 16 + 8),
                                  create_debris)
                        )
                    case 5:  # plate
                        self.tiles.add(
                            Tile(self.plate_img, (x * 16, y * 16 + 8))
                        )
                    case 10:  # question block (coin)
                        self.tiles.add(
                            QuestionBlock((x * 16, y * 16 + 8), create_spinning_coin,
                                        add_coin, add_powerup)
                        )
                    case 11:  # question block (power-up)
                        self.tiles.add(
                            QuestionBlock((x * 16, y * 16 + 8), create_spinning_coin,
                                        add_coin, add_powerup, True)
                        )
                    case 12:  # coin
                        self.coins.add(
                            Coin((x * 16 + 2, y * 16 + 8), 'red')
                        )
                    case 13:  # pipe (top)
                        self.tiles.add(
                            Tile(self.pipe_img_0, (x * 16, y * 16 + 8))
                        )
                    case 14:  # pipe (top entrance)
                        self.tiles.add(
                            Tile(self.pipe_img_0, (x * 16, y * 16 + 8))
                        )
                    case 15:  # pipe (middle)
                        self.tiles.add(
                            Tile(self.pipe_img_1, (x * 16, y * 16 + 8))
                        )
                    case 20:  # player
                        player_pos = (x * 16 - 8, y * 16 + 8)
                    case 21:  # goomba
                        self.enemies.add(
                            Goomba(x * 16, y * 16 + 8, 'red')
                        )
                    case 22:  # goomba (little bit to the left)
                        self.enemies.add(
                            Goomba(x * 16 - 8, y * 16 + 8, 'red')
                        )
                    case 23:  # koopa
                        self.enemies.add(
                            Koopa(x * 16, y * 16 + 8)
                        )
                    case 30:  # hill (small)
                        self.decorations.add(
                            Decoration((x * 16, y * 16 + 21), self.hill_img_0)
                        )
                    case 31:  # hill (large)
                        self.decorations.add(
                            Decoration((x * 16, y * 16 + 21), self.hill_img_1)
                        )
                    case 32:  # bush (small)
                        self.decorations.add(
                            Decoration((x * 16 - 8, y * 16 + 8), self.bush_img_0)
                        )
                    case 33:  # bush (medium)
                        self.decorations.add(
                            Decoration((x * 16 - 8, y * 16 + 8), self.bush_img_1)
                        )
                    case 34:  # bush (large)
                        self.decorations.add(
                            Decoration((x * 16 - 8, y * 16 + 8), self.bush_img_2)
                        )
                    case 35:  # cloud (small)
                        self.decorations.add(
                            Decoration((x * 16 + 8, y * 16 + 8), self.cloud_img_0)
                        )
                    case 36:  # cloud (medium)
                        self.decorations.add(
                            Decoration((x * 16 + 8, y * 16 + 8), self.cloud_img_1)
                        )
                    case 37:  # cloud (large)
                        self.decorations.add(
                            Decoration((x * 16 + 8, y * 16 + 8), self.cloud_img_2)
                        )
        return player_pos

    def draw(self, scroll: int) -> None:
        """Draw all tiles onto screen."""
        for decoration in self.decorations:
            decoration.draw(self.screen, scroll)

        for tile in self.tiles:
            tile.draw(self.screen, scroll)
