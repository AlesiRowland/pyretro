import pygame.display

from pyretro.snake.const import DEFAULT_GAME_SETTINGS
from pyretro.snake.engine import SnakeEngine

if __name__ == "__main__":

    engine = SnakeEngine(pygame.display.set_mode((400, 400)), DEFAULT_GAME_SETTINGS)
    engine.run()
