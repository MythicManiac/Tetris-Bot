PLAY_AREA = (8, 8)
BLOCK_SIZE = 48


class RenderLayers(object):
    BACKGROUND = "background"
    SNAKE = "snake"

    DRAW_ORDER = [
        BACKGROUND,
        SNAKE,
    ]
