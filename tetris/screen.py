import pygame


class Screen(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

    def update(self):
        pygame.display.flip()
