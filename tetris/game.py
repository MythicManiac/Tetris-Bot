import pygame
from collections import defaultdict

from .screen import Screen
from .content import ContentLoader
from .game_interface import GameInterface
from .constants import RenderLayers
from .objects.background import Background
from .objects.pieces import get_random_piece_class

BLOCK_SIZE = 48
PLAY_AREA = (8, 16)


class HeadlessGame(GameInterface):

    def __init__(self, **kwargs):
        self.should_exit = False
        self.game_objects = set()

    def init_game(self):
        self.create_object(get_random_piece_class())

    def update(self):
        for obj in self.game_objects:
            obj.update()

    def create_object(self, object_class, **kwargs):
        obj = object_class(game_interface=self, **kwargs)
        self.game_objects.add(obj)
        return obj

    def destroy_object(self, obj):
        self.game_objects.remove(obj)

    def run(self):
        self.init_game()
        while not self.should_exit:
            self.update()


class Game(HeadlessGame):

    def __init__(self, content_path, **kwargs):
        super(Game, self).__init__(**kwargs)
        pygame.init()
        self.screen = Screen(
            width=PLAY_AREA[0] * BLOCK_SIZE,
            height=PLAY_AREA[1] * BLOCK_SIZE
        )
        self.content_loader = ContentLoader(content_path)
        self.render_layers = defaultdict(set)

    def init_game(self):
        super(Game, self).init_game()
        self.create_object(Background)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_exit = True
        super(Game, self).update()
        self.render()

    def create_object(self, object_class, **kwargs):
        obj = super(Game, self).create_object(object_class, **kwargs)
        obj.load_content(content_loader=self.content_loader)
        layer = obj.get_render_layer()
        if layer is not None:
            self.render_layers[layer].add(obj)
        return obj

    def destroy_object(self, obj):
        layer = obj.get_render_layer
        if layer is not None:
            self.render_layers[layer].remove(obj)
        super(Game, self).destroy_object(obj)

    def render(self):
        for layer in RenderLayers.DRAW_ORDER:
            for obj in self.render_layers[layer]:
                obj.render(self.screen)
        self.screen.update()
