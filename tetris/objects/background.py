import math

from ..constants import RenderLayers
from ..game_object import GameObject, Vector2


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
                draw_pos = Vector2(
                    x=x * self.tile_texture.get_width(),
                    y=y * self.tile_texture.get_height()
                )
                screen.blit(self.tile_texture, draw_pos)
