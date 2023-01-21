# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import logging

import pygame.display

from pyretro.snake import change_log_level
from pyretro.snake.const import GRID_N, UNIT_SIZE
from pyretro.snake.controller import SnakeGameController
from pyretro.snake.model import SnakeGameModel
from pyretro.snake.model.settings import SnakeSettings
from pyretro.snake.view import SnakeGameView


def snake():
    settings = SnakeSettings(UNIT_SIZE, GRID_N)
    model = SnakeGameModel(settings)
    pygame.init()
    surface = pygame.display.set_mode(model.screen_size.to_tuple())
    view = SnakeGameView(surface)
    controller = SnakeGameController(model, view)
    controller.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    change_log_level(logging.DEBUG)
    snake()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
