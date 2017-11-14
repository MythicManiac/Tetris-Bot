PLAY_AREA = (8, 16)
BLOCK_SIZE = 48


class RenderLayers(object):
    BACKGROUND = "background"
    PIECES = "pieces"

    DRAW_ORDER = [
        BACKGROUND,
        PIECES,
    ]
