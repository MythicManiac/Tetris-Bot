# TODO: Delete this top level import, or make sure it's not imported for headless
import pygame

from engine.controller import Controller
from engine.game_object import Vector2


class SnakeController(Controller):

    def __init__(self):
        self.direction = Vector2(x=1, y=0)

    def update(self):
        pass

    def get_direction(self):
        return self.direction


class SnakeHumanController(SnakeController):

    def update(self):
        state = pygame.key.get_pressed()
        if state[pygame.K_UP]:
            self.direction = Vector2(x=0, y=-1)
        elif state[pygame.K_DOWN]:
            self.direction = Vector2(x=0, y=1)
        elif state[pygame.K_LEFT]:
            self.direction = Vector2(x=-1, y=0)
        elif state[pygame.K_RIGHT]:
            self.direction = Vector2(x=1, y=0)


class SnakeAIController(SnakeController):

    def update(self):
        pass
