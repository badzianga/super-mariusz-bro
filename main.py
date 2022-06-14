from sys import exit
from time import time

import pygame
from pygame import mixer
from pygame.constants import K_ESCAPE, K_F11, K_F12, K_RETURN, KEYDOWN, QUIT

from libs.constants import (DISPLAY_SIZE, LEVEL_STATE, LOADING_STATE,
                            MENU_STATE, PHYSICS_FPS, SCREEN_SIZE)
from libs.controller import Controller


def main() -> None:
    mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    pygame.display.set_caption("Super Mariusz Bro")
    pygame.display.set_icon(pygame.image.load("img/icon.png").convert_alpha())

    display = pygame.Surface(DISPLAY_SIZE)
    controller = Controller(display, clock)
    last_time = time()

    lock_fps = False
    smooth_graphics = False

    while True:
        dt = (time() - last_time) * PHYSICS_FPS
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
                elif event.key == K_RETURN:
                    if controller.current_state == LEVEL_STATE:
                        controller.pause()
                    elif controller.current_state == MENU_STATE:
                        controller.switch_state(LOADING_STATE)
                elif event.key == K_F12:
                    lock_fps = not lock_fps
                elif event.key == K_F11:
                    smooth_graphics = not smooth_graphics

        if smooth_graphics:
            surf = pygame.transform.scale2x(display)
        else:
            surf = display.copy()
        
        screen.blit(pygame.transform.scale(surf, SCREEN_SIZE), (0, 0))
        pygame.display.update()
        if lock_fps:
            clock.tick(60)
        else:
            clock.tick()


if __name__ == "__main__":
    main()
