import pygame

from pyretro.langtons_ant.grid import Grid


class Controller:
    def __init__(self, grid: Grid, surface: pygame.Surface):
        self._grid = grid
        self._surface = surface

    def run(self):
        self._grid.draw_onto(self._surface)
        pygame.display.flip()
        while True:
            self._grid.move_ant()
            self._grid.draw_onto(self._surface)
            pygame.display.flip()
