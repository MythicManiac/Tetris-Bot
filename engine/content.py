import pygame
import os


class ContentLoader(object):

    def __init__(self, content_root):
        self.content_root = content_root
        self.content_map = {}

    def load_texture(self, content_path):
        """
        Loads the specified content path as a texture and returns it
        If the content has already been cached, return it straight away
        """
        content = self.content_map.get(content_path)
        if content is not None:
            return content
        content = pygame.image.load(os.path.join(self.content_root, content_path)).convert_alpha()
        self.content_map[content_path] = content
        return content
