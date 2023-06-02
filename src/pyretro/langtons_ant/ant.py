import dataclasses
from typing import cast

import pygame

from pyretro.langtons_ant.enums import Direction


@dataclasses.dataclass
class Coordinates:
    x: int
    y: int

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__dict__ == other.__dict__


class Ant:
    def __init__(
            self,
            size: int,
            coordinates: Coordinates = Coordinates(0, 0),  # These are top left coordinates!
            direction: Direction = Direction.UP,
            color: str = "red",
    ):
        self._size = size
        self._coordinates = coordinates
        self._direction = cast(int, direction.value)
        self.color = color

    @property
    def radius(self):
        return self._size // 2

    @property
    def center(self):
        x, y = self.coordinates
        x *= self._size
        y *= self._size

        return Coordinates(x + (self._size // 2), y + (self._size // 2))

    def rotate_left(self):
        self._direction = self._direction - 1
        if self._direction < 0:
            self._direction += 4

    def rotate_right(self):
        self._direction = (self._direction + 1) % 4
        return self

    @property
    def direction(self):
        return Direction(self._direction)

    @property
    def coordinates(self):
        return self._coordinates

    def move(self, amount: int = 1):
        direction = self.direction
        if direction is Direction.UP:
            self._coordinates.y -= amount
        elif direction is Direction.RIGHT:
            self._coordinates.x += amount
        elif direction is Direction.DOWN:
            self._coordinates.y += amount
        elif direction is Direction.LEFT:
            self._coordinates.x -= amount
        else:
            raise TypeError("Private attribute found to be of type %s", type(self._direction))

    def draw_onto(self, surface):
        pygame.draw.circle(surface, self.color, tuple(self.center), self.radius)
