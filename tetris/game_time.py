import time


class GameTime(object):

    def __init__(self):
        self.start_time = None
        self.last_step_start = None
        self.last_step_end = None
        self.last_step_delta = None

    def _get_time(self):
        return time.monotonic()

    def start(self):
        _time = self._get_time()
        self.start_time = _time
        self.last_step_start = _time
        self.last_step_end = _time
        self.last_step_delta = self.last_step_end - self.last_step_start

    def step_start(self):
        self.last_step_start = self._get_time()

    def step_end(self):
        self.last_step_end = self._get_time()
        self.last_step_delta = self.last_step_end - self.last_step_start

    def get_time_since_last_start(self):
        return self._get_time() - self.last_step_start

    def sleep(self, duration):
        time.sleep(duration)
