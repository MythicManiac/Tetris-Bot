from .game_interface import GameInterface


class Vector2(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, key):
        if key in (0, "x"):
            return self.x
        if key in (1, "y"):
            return self.y
        raise KeyError("Vector2 has no key %s" % key)

    def __setitem__(self, key, value):
        raise RuntimeError("No __setitem__ allowed on Vector2")

    def __len__(self):
        return 2

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        if isinstance(other, tuple):
            return Vector2(self.x * other[0], self.y * other[1])
        if isinstance(other, dict):
            return Vector2(self.x * other["x"], self.y * other["y"])
        return Vector2(self.x * other, self.y * other)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple):
            return Vector2(self.x + other[0], self.y + other[1])
        if isinstance(other, dict):
            return Vector2(self.x + other["x"], self.y + other["y"])
        return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other, self.y - other)
        if isinstance(other, tuple):
            return Vector2(self.x - other[0], self.y - other[1])
        if isinstance(other, dict):
            return Vector2(self.x - other["x"], self.y - other["y"])
        return Vector2(self.x - other, self.y - other)


class GameObject(object):

    def __init__(self, game_interface, *args, **kwargs):
        assert isinstance(game_interface, GameInterface)
        self.game_interface = game_interface
        self.init(*args, **kwargs)

    def init(self):
        pass

    def load_content(self, content_loader):
        pass

    def update(self):
        pass

    def get_render_layer(self):
        pass

    def render(self, screen):
        pass

    @classmethod
    def destroy(cls, obj):
        obj.game_interface.destroy_object(obj)

    @classmethod
    def instantiate(cls, game_interface, object_class, *args, **kwargs):
        game_interface.create_object(object_class, *args, **kwargs)
