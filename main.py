import inspect
import os

from tetris.game import Game


root_path = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
tetris_path = os.path.join(root_path, "tetris")
content_path = os.path.join(tetris_path, "content")

game = Game(content_path=content_path)
game.run()
