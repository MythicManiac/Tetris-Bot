import sys
import os

import numpy as np
import gym
import gym.envs
from six import StringIO

from engine.game_object import Vector2
from .snake import SnakeHeadlessGame, SnakeGame
from .objects.snake_head import SnakeHead, SnakePiece, Cherry
from .constants import PLAY_AREA


ENV_NAMES = {
    "small": "SnakeSmall-v0",
    "normal": "Snake-v0",
}


class SnakeGameState(object):
    """
    Features
    Snake piece ages
    Head location 1-hot
    Head next location 1-hot
    Cherry location 1-hot.
    """

    def __init__(self, width, height, headless=False):
        if (height, width) != PLAY_AREA:
            raise ValueError("Only dimensions {} supported".format(PLAY_AREA))
        self.shape = (4, width, height)
        self.width = width
        self.height = height

        self.game_class = SnakeHeadlessGame if headless else SnakeGame
        self.game_kwargs = {}
        if not headless:
            self.game_kwargs["content_path"] = os.path.abspath(
                os.path.join("snake", "content")
            )
        self.seed()

    @property
    def pieces(self):
        result = set()
        for obj in self.game.game_objects:
            if isinstance(obj, SnakePiece):
                result.add(obj)
        return result

    @property
    def head(self):
        for obj in self.game.game_objects:
            if isinstance(obj, SnakeHead):
                return obj
        raise KeyError("Snake head not found")

    @property
    def cherry(self):
        for obj in self.game.game_objects:
            if isinstance(obj, Cherry):
                return obj
        raise KeyError("Cherry not found")

    def reset(self):
        self.game = self.game_class(**self.game_kwargs)
        self.game._init_game()

    def step(self, direction):
        self.game.controller.direction = direction
        last_lenght = self.head.length
        self.game._run_step()
        if self.head.length > last_lenght:
            return 1
        if self.game.should_exit:
            return -1
        return 0

    def seed(self, seed=None):
        self.random_seed = seed if seed else 1234
        self.game_kwargs["random_seed"] = self.random_seed
        return self.random_seed

    def render_ansi(self, outfile):
        features = self.encode()
        for x in range(2 * self.width + 3):
            outfile.write("#")
        outfile.write("\n")
        for y in range(self.height):
            outfile.write("# ")
            for x in range(self.width):
                if features[0][y][x]:
                    outfile.write("O ")
                elif features[1][y][x]:
                    outfile.write("@ ")
                elif features[3][y][x]:
                    outfile.write("% ")
                else:
                    outfile.write(". ")
            outfile.write("#\n")
        for x in range(2 * self.width + 3):
            outfile.write("#")
        outfile.write("\n")

    def encode(self):
        features = np.zeros(self.shape)
        for piece in self.pieces:
            x, y = piece.position
            features[0][y][x] = piece.age + 1
        x, y = self.head.position
        features[1][y][x] = 1
        x, y = self.head.position + self.head.direction
        x %= self.width
        y %= self.height
        features[2][y][x] = 1
        x, y = self.cherry.position
        features[3][y][x] = 1

        return features


class SnakeEnv(gym.Env):
    metadata = {"render.modes": ["human", "ansi"]}

    def __init__(self, height, width):
        self.state = SnakeGameState(width, height)

        self.reward_range = (-1, 1)
        self.action_space = gym.spaces.Discrete(4)

        max_age = height * width
        self.observation_space = gym.spaces.Box(
            low=0,
            high=max_age,
            shape=self.state.shape,
            dtype=np.float32
        )
        self.seed()

    def seed(self, seed=None):
        return [self.state.seed(seed)]

    def reset(self):
        self.state.reset()
        return self.state.encode()

    def render(self, mode="human"):
        outfile = StringIO() if mode == "ansi" else sys.stdout
        self.state.render_ansi(outfile)
        return outfile

    def close(self):
        return

    def step(self, action):
        direction = Vector2(0, 0)
        if action == 0:
            direction.x = 1
        elif action == 1:
            direction.x = -1
        elif action == 2:
            direction.y = 1
        elif action == 3:
            direction.y = -1
        else:
            raise ValueError("Action not in action space")
        reward = self.state.step(direction)
        observation = self.state.encode()
        return observation, reward, (reward < 0), {"state": self.state}


def register():
    gym.envs.register(
        id=ENV_NAMES["small"],
        entry_point="snake.env:SnakeEnv",
        kwargs={"width": 4, "height": 4},
        max_episode_steps=None,
        reward_threshold=25.0,
    )
    gym.envs.register(
        id=ENV_NAMES["normal"],
        entry_point="snake.env:SnakeEnv",
        kwargs={"width": 10, "height": 10},
        max_episode_steps=None,
        reward_threshold=25.0,
    )
