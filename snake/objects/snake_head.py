from engine.game_object import GameObject, Vector2
from ..constants import RenderLayers, PLAY_AREA


class Level(GameObject):

    def init(self):
        self.head = self.create_snake_head()
        self.cherry = self.create_cherry()
        self.piece_positions = set()

    def on_cherry_eaten(self):
        self.cherry = self.create_cherry()

    def create_cherry(self):
        return GameObject.instantiate(
            self.game_interface,
            Cherry,
            level=self,
            position=Vector2(5, 5)
        )

    def create_snake_head(self):
        return GameObject.instantiate(
            self.game_interface,
            SnakeHead,
            level=self
        )

    def add_piece_position(self, position):
        self.piece_positions.add(position)

    def remove_piece_position(self, position):
        self.piece_positions.remove(position)


class SnakeHead(GameObject):

    def init(self, level):
        self.level = level
        self.position = Vector2(0, 0)
        self.direction = Vector2(1, 0)
        self.length = 3

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

    def update_input(self, controller):
        self.direction = controller.get_direction()

    def on_cherry_eaten(self):
        self.level.cherry.on_being_eaten()
        self.length += 1
        # TODO: Reward AI?

    def update(self):
        old_pos = self.position.clone()
        self.position += self.direction

        if self.position == self.level.cherry.position:
            self.on_cherry_eaten()

        GameObject.instantiate(
            self.game_interface,
            SnakePiece,
            level=self.level,
            position=old_pos,
            head=self
        )

        if self.position.x >= PLAY_AREA[0]:
            self.position.x = 0
        if self.position.y >= PLAY_AREA[1]:
            self.position.y = 0


class SnakePiece(GameObject):

    def init(self, level, position, head):
        self.level = level
        self.position = position
        self.head = head
        self.age = 0
        self.level.add_piece_position(self.position)

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
        self.age += 1
        if self.head.length - self.age <= 0:
            self.level.remove_piece_position(self.position)
            GameObject.destroy(self)


class Cherry(GameObject):

    def init(self, level, position):
        self.level = level
        self.position = position

    def load_content(self, content_loader):
        self.tile_texture = content_loader.load_texture("piece-purple.png")

    def get_render_layer(self):
        return RenderLayers.SNAKE

    def on_being_eaten(self):
        self.level.on_cherry_eaten()
        GameObject.destroy(self)

    def render(self, screen):
        draw_pos = self.position * (
            self.tile_texture.get_width(),
            self.tile_texture.get_height()
        )
        screen.blit(self.tile_texture, draw_pos)
