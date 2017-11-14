import pygame

from .screen import Screen
from .content import ContentLoader

BLOCK_SIZE = 48
PLAY_AREA = (8, 16)


class HeadlessGame(object):

    def __init__(self):
        self.should_exit = False
        self.game_objects = []

    def update(self):
        for obj in self.game_objects:
            obj.update()

    def create_object(self, object_class, **kwargs):
        obj = object_class(**kwargs)
        return obj

    def run(self):
        while not self.should_exit:
            self.update()


class Game(HeadlessGame):

    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        self.screen = Screen(PLAY_AREA[0] * BLOCK_SIZE, PLAY_AREA[1] * BLOCK_SIZE)
        self.content_loader = ContentLoader("asd")

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_exit = True
        super(Game, self).update()
        self.render()

    def create_object(self, object_class, **kwargs):
        obj = super(Game, self).create_object(object_class, **kwargs)
        obj.load_content(content_loader=self.content_loader)
        return obj

    def render(self):
        for obj in self.game_objects:
            obj.render(self.screen)
        self.screen.update()
