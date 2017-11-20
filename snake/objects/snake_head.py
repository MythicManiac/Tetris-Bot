from engine.game_object import GameObject, Vector2
from ..constants import RenderLayers, PLAY_AREA


class SnakeHead(GameObject):

    def init(self):
        self.position = Vector2(0, 0)

    def load_content(self, content_loader):
        self.tile_texture = content_loader.load_texture("piece-blue.png")

    def get_render_layer(self):
        return RenderLayers.SNAKE

    def render(self, screen):
        draw_pos = self.position * (
            self.tile_texture.get_width(),
            self.tile_texture.get_height()
        )
        screen.blit(self.tile_texture, draw_pos)

    def update(self):
        old_pos = self.position.clone()
        self.position.x += 1

        # if something eaten:
        # remove eaten
        GameObject.instantiate(self.game_interface, SnakePiece, position=old_pos)

        if self.position.x >= PLAY_AREA[0]:
            self.position.x = 0
        if self.position.y >= PLAY_AREA[1]:
            self.position.y = 0


class SnakePiece(GameObject):

    def init(self, position):
        self.position = position

    def load_content(self, content_loader):
        self.tile_texture = content_loader.load_texture("piece-blue.png")

    def get_render_layer(self):
        return RenderLayers.SNAKE

    def render(self, screen):
        draw_pos = self.position * (
            self.tile_texture.get_width(),
            self.tile_texture.get_height()
        )
        screen.blit(self.tile_texture, draw_pos)
