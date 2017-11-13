
class Orientations(object):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"


class BasePiece(object):

    def __init__(self):
        pass


class IPiece(BasePiece):
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
