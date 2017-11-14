import pygame

from .screen import Screen

BLOCK_SIZE = 48
PLAY_AREA = (8, 16)


class Game(object):

    def __init__(self, headless=False):
        self.headless = headless
        self._headless_init()
        if not headless:
            self._headful_init()

    def _headless_init(self):
        self.should_exit = False
        self.game_objects = []

    def _headful_init(self):
        pygame.init()
        self.screen = Screen(PLAY_AREA[0] * BLOCK_SIZE, PLAY_AREA[1] * BLOCK_SIZE)

    def update(self):
        if not self.headless:
            self._headful_update()
        self._headless_update()

    def _headless_update(self):
        for obj in self.game_objects:
            obj.update()

    def _headful_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_exit = True
        self.screen.update()

    def render(self):
        if self.headless:
            return

    def run(self):
        while not self.should_exit:
            self.update()
