import math

from .constants import RenderLayers


class GameObject(object):

    def __init__(self, game_interface, *args, **kwargs):
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


class Background(GameObject):

    def load_content(self, content_loader):
        self.tile_texture = content_loader.load_texture("background.png")

    def get_render_layer(self):
        return RenderLayers.BACKGROUND

    def render(self, screen):
        tile_width = int(math.ceil(screen.width / self.tile_texture.get_width()))
        tile_height = int(math.ceil(screen.height / self.tile_texture.get_height()))
        for x in range(tile_width):
            for y in range(tile_height):
                draw_pos = (
                    x * self.tile_texture.get_width(),
                    y * self.tile_texture.get_height()
                )
                screen.blit(self.tile_texture, draw_pos)
