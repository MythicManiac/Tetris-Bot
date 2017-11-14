import inspect
import os
import sys


def get_headless_game():
    from tetris.game import HeadlessGame
    return HeadlessGame()


def get_game():
    root_path = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    tetris_path = os.path.join(root_path, "tetris")
    content_path = os.path.join(tetris_path, "content")
    from tetris.game import Game
    return Game(content_path=content_path)


if __name__ == "__main__":
    if "--headless" in sys.argv:
        game = get_headless_game()
    else:
        game = get_game()
    game.run()
