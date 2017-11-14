from .game_interface import GameInterface


class GameObject(object):

    def __init__(self, game_interface, *args, **kwargs):
        assert isinstance(game_interface, GameInterface)
        self.game_interface = game_interface

    def load_content(self, content_loader):
        pass

    def update(self):
        pass

    def get_render_layer(self):
        pass

    def render(self, screen):
        pass

    def destroy(self):
        self.game_interface.destroy(self)
