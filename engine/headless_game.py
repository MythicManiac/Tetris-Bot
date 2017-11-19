from .game_interface import GameInterface
from .game_time import GameTime


class HeadlessGame(GameInterface):

    def __init__(self, *args, **kwargs):
        self.should_exit = False
        self.game_objects = set()
        self.time = GameTime()

    def init_game(self):
        pass

    def post_init_game(self):
        pass

    def update(self):
        for obj in self.game_objects:
            obj.update()

    def create_object(self, object_class, *args, **kwargs):
        obj = object_class(game_interface=self, **kwargs)
        self.game_objects.add(obj)
        return obj

    def destroy_object(self, obj):
        self.game_objects.remove(obj)

    def _run_step(self):
        self.time.step_start()
        self.update()
        self.time.step_end()

    def _can_run_next_step(self):
        return True

    def _extrastep(self):
        pass

    def on_exit(self):
        pass

    def run(self):
        self.init_game()
        self.post_init_game()
        self.time.start()
        while not self.should_exit:
            if self._can_run_next_step():
                self._run_step()
            self._extrastep()
        self.on_exit()
