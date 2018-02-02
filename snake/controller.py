# TODO: Delete this top level import, or make sure it's not imported for headless
import pygame

from engine.controller import Controller
from engine.game_object import Vector2


class SnakeController(Controller):

    def __init__(self):
        self.direction = Vector2(x=1, y=0)

    def update(self):
        pass

    def on_event(self, event_type, event_data):
        pass

    def get_direction(self):
        return self.direction


class SnakeHumanController(SnakeController):

    def on_event(self, event_type, event_data):
        if event_type == "keyboard_keydown":
            if event_data == pygame.K_UP:
                self.direction = Vector2(x=0, y=-1)
            elif event_data == pygame.K_DOWN:
                self.direction = Vector2(x=0, y=1)
            elif event_data == pygame.K_LEFT:
                self.direction = Vector2(x=-1, y=0)
            elif event_data == pygame.K_RIGHT:
                self.direction = Vector2(x=1, y=0)


class SnakeAIController(SnakeController):

    def on_event(self, event_type, event_data):
        pass
