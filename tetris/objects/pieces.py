import random

from engine.game_object import GameObject, Vector2
from ..constants import RenderLayers, BLOCK_SIZE, PLAY_AREA


class Orientations(object):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"


class BasePiece(GameObject):

    def init(self):
        self.position = Vector2(2, 0)
        self.set_orientation(Orientations.UP)

    def set_orientation(self, new_orientation):
        self.orientation = new_orientation
        self.matrix = self.orientations[self.orientation]

    def load_content(self, content_loader):
        self.tile_texture = content_loader.load_texture(self.texture_path)

    def render(self, screen):
        for y, row in enumerate(self.matrix):
            for x, character in enumerate(row):
                if character != "#":
                    continue
                screen.blit(self.tile_texture, (self.position + (x, y)) * BLOCK_SIZE)

    def get_render_layer(self):
        return RenderLayers.PIECES

    def update(self):
        self.position += (0, 1)
        if self.position.y >= PLAY_AREA[1]:
            GameObject.destroy(self)
            GameObject.instantiate(self.game_interface, get_random_piece_class())


class IPiece(BasePiece):
    texture_path = "piece-turqoise.png"
    orientations = {
        Orientations.UP: [
            "    ",
            "####",
            "    ",
            "    ",
        ],
        Orientations.RIGHT: [
            "  # ",
            "  # ",
            "  # ",
            "  # ",
        ],
        Orientations.DOWN: [
            "    ",
            "    ",
            "####",
            "    ",
        ],
        Orientations.LEFT: [
            " #  ",
            " #  ",
            " #  ",
            " #  ",
        ],
    }


class OPiece(BasePiece):
    texture_path = "piece-yellow.png"
    orientations = {
        Orientations.UP: [
            "    ",
            " ## ",
            " ## ",
            "    ",
        ],
        Orientations.RIGHT: [
            "    ",
            " ## ",
            " ## ",
            "    ",
        ],
        Orientations.DOWN: [
            "    ",
            " ## ",
            " ## ",
            "    ",
        ],
        Orientations.LEFT: [
            "    ",
            " ## ",
            " ## ",
            "    ",
        ],
    }


class TPiece(BasePiece):
    texture_path = "piece-purple.png"
    orientations = {
        Orientations.UP: [
            " #  ",
            "### ",
            "    ",
            "    ",
        ],
        Orientations.RIGHT: [
            " #  ",
            " ## ",
            " #  ",
            "    ",
        ],
        Orientations.DOWN: [
            "    ",
            "### ",
            " #  ",
            "    ",
        ],
        Orientations.LEFT: [
            " #  ",
            "##  ",
            " #  ",
            "    ",
        ],
    }


class SPiece(BasePiece):
    texture_path = "piece-green.png"
    orientations = {
        Orientations.UP: [
            " ## ",
            "##  ",
            "    ",
            "    ",
        ],
        Orientations.RIGHT: [
            " #  ",
            " ## ",
            "  # ",
            "    ",
        ],
        Orientations.DOWN: [
            "    ",
            " ## ",
            "##  ",
            "    ",
        ],
        Orientations.LEFT: [
            "#   ",
            "##  ",
            " #  ",
            "    ",
        ],
    }


class ZPiece(BasePiece):
    texture_path = "piece-red.png"
    orientations = {
        Orientations.UP: [
            "##  ",
            " ## ",
            "    ",
            "    ",
        ],
        Orientations.RIGHT: [
            "  # ",
            " ## ",
            " #  ",
            "    ",
        ],
        Orientations.DOWN: [
            "    ",
            "##  ",
            " ## ",
            "    ",
        ],
        Orientations.LEFT: [
            " #  ",
            "##  ",
            "#   ",
            "    ",
        ],
    }


class JPiece(BasePiece):
    texture_path = "piece-blue.png"
    orientations = {
        Orientations.UP: [
            "#   ",
            "### ",
            "    ",
            "    ",
        ],
        Orientations.RIGHT: [
            " ## ",
            " #  ",
            " #  ",
            "    ",
        ],
        Orientations.DOWN: [
            "    ",
            "### ",
            "  # ",
            "    ",
        ],
        Orientations.LEFT: [
            " #  ",
            " #  ",
            "##  ",
            "    ",
        ],
    }


class LPiece(BasePiece):
    texture_path = "piece-orange.png"
    orientations = {
        Orientations.UP: [
            "  # ",
            "### ",
            "    ",
            "    ",
        ],
        Orientations.RIGHT: [
            " #  ",
            " #  ",
            " ## ",
            "    ",
        ],
        Orientations.DOWN: [
            "    ",
            "### ",
            "#   ",
            "    ",
        ],
        Orientations.LEFT: [
            "##  ",
            " #  ",
            " #  ",
            "    ",
        ],
    }


ALL_PIECES = [
    IPiece,
    OPiece,
    TPiece,
    SPiece,
    ZPiece,
    JPiece,
    LPiece
]


def get_random_piece_class():
    return random.choice(ALL_PIECES)
