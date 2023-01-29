from typing import Type, TypeVar

import pygame as pygame

from pyretro.snake.structs import Point, Size

Self = TypeVar("Self", bound="SnakeRect")


class SnakeRect(pygame.Rect):
    """Represents a rect for the Snake Game."""

    def to_tuple(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.width, self.height

    @classmethod
    def from_structs(cls: Type[Self], point: Point, size: Size) -> Self:
        return cls(point.x, point.y, size.width, size.height)