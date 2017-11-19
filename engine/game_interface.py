
class GameInterface(object):

    def destroy_object(self, *args, **kwargs):
        raise NotImplementedError()

    def create_object(self, object_class, *args, **kwargs):
        raise NotImplementedError()
