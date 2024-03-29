from types import FunctionType

from numpy import loadtxt, uint8
from pygame.image import load as load_image
from pygame.sprite import Group
from pygame.surface import Surface

from .coin import Coin
from .enemies import Goomba, Koopa
from .tiles import (Brick, CoinBrick, Decoration, HiddenBlock, QuestionBlock,
                    Tile)


class Level:
    """Object with map data that contains all tiles."""

    def __init__(self, screen: Surface, world: str, theme: str) -> None:
        self.screen = screen

        self.tiles = Group()
        self.coins = Group()
        self.enemies = Group()
        self.decorations = Group()

        # temporary, these will be in Controller in the future
        self.rock_img = load_image(f'img/{theme}/rock_0.png').convert()
        self.block_img = load_image(f'img/{theme}/block_0.png').convert()
        self.brick_img_0 = load_image(f'img/{theme}/brick_0.png').convert()
        self.brick_img_1 = load_image(f'img/{theme}/brick_1.png').convert()
        self.plate_img = load_image(f'img/{theme}/plate_0.png').convert()
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
        self.pipe_img_2 = load_image('img/pipe_2.png').convert_alpha()
        self.pipe_img_3 = load_image('img/pipe_3.png').convert_alpha()
        self.pole_image = load_image('img/pole_0.png').convert_alpha()
        self.castle_image = load_image('img/castle_0.png').convert_alpha()

        # TODO: temporary?
        self.world = world

    def load_level(self, create_spinning_coin: FunctionType,
                   add_coin: FunctionType, create_debris: FunctionType,
                   add_powerup: FunctionType,
                   enemy_kill_animation: FunctionType) -> tuple:
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
                    case 6:  # brick (with coins)
                        self.tiles.add(
                            CoinBrick(self.brick_img_0, (x * 16, y * 16 + 8),
                                      self.plate_img, create_spinning_coin,
                                      add_coin)
                        )
                    case 7:  # hidden block (1up)
                        self.tiles.add(
                            HiddenBlock(( x * 16, y * 16 + 8), self.plate_img, add_powerup)
                        )
                    case 10:  # question block (coin)
                        self.tiles.add(
                            QuestionBlock((x * 16, y * 16 + 8), create_spinning_coin,
                                        add_coin, add_powerup, 'red')
                        )
                    case 11:  # question block (power-up)
                        self.tiles.add(
                            QuestionBlock((x * 16, y * 16 + 8), create_spinning_coin,
                                        add_coin, add_powerup, 'red', True)
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
                    case 16:  # pipe (crossing middle)
                        self.tiles.add(
                            Tile(self.pipe_img_2, (x * 16 - 4, y * 16 + 8))
                        )
                    case 17:  # pipe (left)
                        self.tiles.add(
                            Tile(self.pipe_img_3, (x * 16, y * 16 + 8))
                        )
                    case 20:  # player
                        player_pos = (x * 16 - 8, y * 16 + 8)
                    case 21:  # goomba
                        self.enemies.add(
                            Goomba(x * 16, y * 16 + 8, 'red', enemy_kill_animation)
                        )
                    case 22:  # goomba (little bit to the left)
                        self.enemies.add(
                            Goomba(x * 16 - 8, y * 16 + 8, 'red', enemy_kill_animation)
                        )
                    case 23:  # koopa
                        self.enemies.add(
                            Koopa(x * 16, y * 16 + 8, enemy_kill_animation)
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
                    case 38:  # pole
                        self.decorations.add(
                            Decoration((x * 16 + 8, y * 16), self.pole_image)
                        )
                    case 39:  # castle
                        self.decorations.add(
                            Decoration((x * 16, y * 16 + 8), self.castle_image)
                        )
        return player_pos

    def draw(self, scroll: int) -> None:
        """Draw all tiles onto screen."""
        for decoration in self.decorations:
            decoration.draw(self.screen, scroll)

        for tile in self.tiles:
            tile.draw(self.screen, scroll)
