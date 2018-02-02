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
        return Vector2(self.x * other.x, self.y * other.y)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple):
            return Vector2(self.x + other[0], self.y + other[1])
        if isinstance(other, dict):
            return Vector2(self.x + other["x"], self.y + other["y"])
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other, self.y - other)
        if isinstance(other, tuple):
            return Vector2(self.x - other[0], self.y - other[1])
        if isinstance(other, dict):
            return Vector2(self.x - other["x"], self.y - other["y"])
        return Vector2(self.x - other.x, self.y - other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        if isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        if isinstance(other, dict):
            return self.x == other["x"] and self.y == other["y"]
        return super(Vector2, self).__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def clone(self):
        return Vector2(self.x, self.y)


class GameObject(object):

    def __init__(self, game_interface, *args, **kwargs):
        self.game_interface = game_interface
        self.init(*args, **kwargs)

    def init(self, **kwargs):
        pass

    def load_content(self, content_loader):
        pass

    def update_input(self, controller):
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
        return game_interface.create_object(object_class, *args, **kwargs)
