import pygame
from collections import defaultdict

from .screen import Screen
from .content import ContentLoader
from .headless_game import HeadlessGame


class Game(HeadlessGame):

    def __init__(self, content_path, *args, **kwargs):
        super(Game, self).__init__(**kwargs)
        pygame.init()
        self.screen = Screen(**self.get_screen_params())
        self.content_loader = ContentLoader(content_path)
        self.render_layers = defaultdict(set)

    def get_screen_params(self):
        raise NotImplementedError()

    def get_layer_draw_order(self):
        raise NotImplementedError()

    def post_init_game(self):
        self.render()

    def update(self):
        super(Game, self).update()
        self.render()

    def create_object(self, object_class, *args, **kwargs):
        obj = super(Game, self).create_object(object_class, **kwargs)
        obj.load_content(content_loader=self.content_loader)
        layer = obj.get_render_layer()
        if layer is not None:
            self.render_layers[layer].add(obj)
        return obj

    def destroy_object(self, obj):
        layer = obj.get_render_layer()
        if layer is not None:
            self.render_layers[layer].remove(obj)
        super(Game, self).destroy_object(obj)

    def render(self):
        for layer in self.get_layer_draw_order():
            for obj in self.render_layers[layer]:
                obj.render(self.screen)
        self.screen.update()

    def _can_run_next_step(self):
        return self.time.get_time_since_last_step_start() >= 0.32

    def _extrastep(self):
        super(Game, self)._extrastep()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_exit = True
