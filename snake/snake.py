from engine.game import Game, HeadlessGame

from .constants import RenderLayers, BLOCK_SIZE, PLAY_AREA
from .objects.background import Background
from .objects.snake_head import Level
from .controller import SnakeHumanController, SnakeAIController


class SnakeMixin(object):
    def get_screen_params(self):
        return {
            "width": PLAY_AREA[0] * BLOCK_SIZE,
            "height": PLAY_AREA[1] * BLOCK_SIZE,
        }

    def get_layer_draw_order(self):
        return RenderLayers.DRAW_ORDER

    def get_step_rate(self):
        return 0.08

    def init_game(self):
        super(SnakeMixin, self).init_game()
        self.create_object(Level)
        self.create_object(Background)

    def on_exit(self):
        print(self.time.get_average_steps_per_second())


class SnakeHeadlessGame(SnakeMixin, HeadlessGame):
    def get_controller_class(self):
        return SnakeAIController


class SnakeGame(SnakeMixin, Game):
    def get_controller_class(self):
        return SnakeHumanController
