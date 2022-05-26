from sys import exit
from time import time

import pygame
from pygame import mixer
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT

from libs.constants import DISPLAY_SIZE, FPS, SCREEN_SIZE
from libs.controller import Controller


def main() -> None:
    pygame.init()
    mixer.pre_init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    pygame.display.set_caption("Super Mariusz Bro")
    pygame.display.set_icon(pygame.image.load("img/icon.png").convert_alpha())

    display = pygame.Surface(DISPLAY_SIZE)
    controller = Controller(display, clock)
    last_time = time()

    while True:
        dt = (time() - last_time) * FPS
        last_time = time()

        controller.run(dt)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

        screen.blit(pygame.transform.scale(display, SCREEN_SIZE), (0, 0))
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    main()
