import numpy as np
import pygame.draw

from pyretro.langtons_ant.ant import Ant, Coordinates
from pyretro.langtons_ant.enums import SquareColor


class GridSpec:
    def __init__(self, square_n, grid_n):
        self.square_n = square_n
        self.grid_n = grid_n

    @property
    def square_size(self) -> tuple[int, int]:
        return self.square_n, self.square_n

    @property
    def grid_size(self) -> tuple[int, int]:
        return self.grid_n, self.grid_n


class Grid:
    def __init__(self, ant: Ant, grid_spec: GridSpec) -> None:
        self._ant = ant
        self._grid_spec = grid_spec

        self._arr = np.full(grid_spec.grid_size, SquareColor.WHITE)

    def move_ant(self):
        coordinates = self._ant.coordinates

        if self._arr[tuple(coordinates)] is SquareColor.WHITE:
            self._ant.rotate_right()
            self._arr[tuple(coordinates)] = SquareColor.BLACK
        elif self._arr[tuple(coordinates)] is SquareColor.BLACK:
            self._ant.rotate_left()
            self._arr[tuple(coordinates)] = SquareColor.WHITE
        else:
            raise TypeError("Square is of type %s", type(self._arr[coordinates[coordinates]]))

        self._ant.move()

    def iter_squares(self):
        yield from (square for row in self._arr for square in row)

    def get_color(self, coordinates: tuple[int, int]):
        x, y = coordinates
        square = self._arr[x, y]

        if square is SquareColor.WHITE:
            return "white"
        elif square is SquareColor.BLACK:
            return "black"
        else:
            raise TypeError("incorrect type %s", type(square))

    def get_pixel_coordinates(self, grid_coordinates):
        x_mul, y_mul = self._grid_spec.square_size
        return Coordinates(grid_coordinates.x * x_mul, grid_coordinates.y * y_mul)

    def draw_onto(self, surface):
        n1, n2 = self._grid_spec.grid_size
        for i in range(n1):
            for j in range(n2):
                color = self.get_color((i, j))
                pixel_coordinates = self.get_pixel_coordinates(Coordinates(i, j))
                rect = pygame.rect.Rect(pixel_coordinates.x, pixel_coordinates.y, self._grid_spec.square_n, self._grid_spec.square_n)
                pygame.draw.rect(surface, color, rect)

        # self._ant.draw_onto(surface)