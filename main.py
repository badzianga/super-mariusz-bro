from sys import exit

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT

from libs.constants import BG_COLOR, FPS, SCREEN_SIZE


def main():
    # initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    pygame.display.set_caption("Super Mariusz Bro")
    pygame.display.set_icon(pygame.image.load("img/icon.png").convert_alpha())

    while True:
        screen.fill(BG_COLOR)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
