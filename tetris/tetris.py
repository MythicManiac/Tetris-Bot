from engine.game import Game, HeadlessGame

from .constants import RenderLayers, BLOCK_SIZE, PLAY_AREA
from .objects.background import Background
from .objects.pieces import get_random_piece_class


class TetrisMixin(object):
    def get_screen_params(self):
        return {
            "width": PLAY_AREA[0] * BLOCK_SIZE,
            "height": PLAY_AREA[1] * BLOCK_SIZE,
        }

    def get_layer_draw_order(self):
        return RenderLayers.DRAW_ORDER

    def init_game(self):
        super(TetrisMixin, self).init_game()
        self.create_object(get_random_piece_class())
        self.create_object(Background)

    def _extrastep(self):
        super(TetrisMixin, self)._extrastep()
        if self.time.get_time_since_start() > 10:
            self.should_exit = True

    def on_exit(self):
        print(self.time.get_average_steps_per_second())


class TetrisHeadlessGame(TetrisMixin, HeadlessGame):
    pass


class TetrisGame(TetrisMixin, Game):
    pass
