import sys
import pygame


BLOCK_SIZE = 48


class Screen(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((width * BLOCK_SIZE, height * BLOCK_SIZE))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()

SCREEN = Screen(8, 16)
