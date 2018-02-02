from engine.game import Game, HeadlessGame

from .constants import RenderLayers, BLOCK_SIZE, PLAY_AREA
from .objects.background import Background
from .objects.snake_head import SnakeHead
from .controller import SnakeHumanController, SnakeAIController


class SnakeMixin(object):
    def get_screen_params(self):
        return {
            "width": PLAY_AREA[0] * BLOCK_SIZE,
            "height": PLAY_AREA[1] * BLOCK_SIZE,
        }

    def get_layer_draw_order(self):
        return RenderLayers.DRAW_ORDER

    def init_game(self):
        super(SnakeMixin, self).init_game()
        self.create_object(SnakeHead)
        self.create_object(Background)

    def _extrastep(self):
        super(SnakeMixin, self)._extrastep()
        if self.time.get_time_since_start() > 10:
            self.should_exit = True

    def on_exit(self):
        print(self.time.get_average_steps_per_second())


class SnakeHeadlessGame(SnakeMixin, HeadlessGame):
    def get_controller_class(self):
        return SnakeAIController


class SnakeGame(SnakeMixin, Game):
    def get_controller_class(self):
        return SnakeHumanController
