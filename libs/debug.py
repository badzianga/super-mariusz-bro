from pygame.font import Font
from pygame.surface import Surface
from pygame.time import Clock

from .constants import RED


class Debug:
    def __init__(self, screen: Surface, clock: Clock) -> None:
        self.screen = screen
        self.clock = clock
        self.font = Font("fonts/PressStart2P.ttf", 8)

    def draw(self) -> None:
        surf = self.font.render(str(int(self.clock.get_fps())), False, RED)
        self.screen.blit(surf, (0, 0))
