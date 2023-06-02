import pygame.display

from pyretro.langtons_ant.ant import Ant, Coordinates
from pyretro.langtons_ant.controller import Controller
from pyretro.langtons_ant.grid import Grid, GridSpec


def main():
    grid_spec = GridSpec(10, 100)
    ant = Ant(8, Coordinates(50, 50))
    grid = Grid(ant, grid_spec)
    surface = pygame.display.set_mode((1000, 1000))
    controller = Controller(grid, surface)
    controller.run()

if __name__ == "__main__":
    main()