from .game_time import GameTime
from .controller import Controller
from .random import Random


class HeadlessGame(object):

    def __init__(self, random_seed=1234, *args, **kwargs):
        self.should_exit = False
        self.game_objects = set()
        self.created_game_objects = []
        self.destroyed_game_objects = []
        self.controller = self.get_controller_class()()
        self.random = Random(random_seed=random_seed)
        self.time = GameTime()

    def get_controller_class(self):
        return Controller

    def init_game(self):
        pass

    def on_exit(self):
        pass

    def call_controller_event(self, event_type, event_data):
        self.controller.on_event(event_type, event_data)

    def create_object(self, object_class, *args, **kwargs):
        obj = object_class(game_interface=self, **kwargs)
        self.created_game_objects.append(obj)
        return obj

    def destroy_object(self, obj):
        self.destroyed_game_objects.append(obj)

    def _update(self):
        self.controller.update()
        for obj in self.game_objects:
            obj.update_input(self.controller)
            obj.update()

    def _handle_created_object(self, obj):
        self.game_objects.add(obj)

    def _handle_destroyed_object(self, obj):
        self.game_objects.remove(obj)

    def _map_object_changes(self):
        for obj in self.created_game_objects:
            self._handle_created_object(obj)
        self.created_game_objects = []
        for obj in self.destroyed_game_objects:
            self._handle_destroyed_object(obj)
        self.destroyed_game_objects = []

    def _run_step(self):
        self.time.step_start()
        self._update()
        self._map_object_changes()
        self._render()
        self.time.step_end()

    def _can_run_next_step(self):
        return True

    def _extrastep(self):
        pass

    def _init_game(self):
        self.time.start()
        self.init_game()
        self._map_object_changes()
        self._render()

    def _render(self):
        pass

    def run(self):
        self._init_game()
        while not self.should_exit:
            if self._can_run_next_step():
                self._run_step()
            self._extrastep()
        self.on_exit()
