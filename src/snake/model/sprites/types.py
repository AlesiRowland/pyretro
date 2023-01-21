import abc
import logging
from copy import copy
from typing import TypeVar

from snake.model.sprites.rect import SnakeRect
from snake.model.structs import Point, Size

Self = TypeVar("Self", bound="SnakeRect")

LOGGER = logging.getLogger(__name__)


class Sprite(abc.ABC):
    color: str = NotImplemented

    @property
    @abc.abstractmethod
    def rects(self) -> list[SnakeRect]:
        ...

    def __len__(self) -> int:
        return len(self.rects)

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.rects == other.rects


class SnakeFood(Sprite):
    color = "red"

    def __init__(self, snake_rect: SnakeRect) -> None:
        self._rect = snake_rect

    @property
    def rects(self) -> list[SnakeRect]:
        return [self._rect]

    def __str__(self):
        return f"{type(self).__name__}({self._rect})"


class Snake(Sprite):
    color = "purple"

    def __init__(self, head: SnakeRect, screen_size: Size) -> None:
        self._rects = [head]
        self._screen_size = screen_size

    @property
    def rects(self) -> list[SnakeRect]:
        return self._rects

    @property
    def head(self) -> SnakeRect:
        return self._rects[0]

    @property
    def tail(self) -> list[SnakeRect]:
        return self._rects[1:]

    def move(self, new_head_coordinates: Point) -> None:
        LOGGER.debug("Moving Snake to %s:", new_head_coordinates)
        new = self._rects.pop()
        new.update(new_head_coordinates.to_tuple(), self.head.size)
        self._rects.insert(0, new)

    def grow(self, new_head_coordinates: Point) -> None:
        LOGGER.debug("Growing Snake to coordinates: %s", new_head_coordinates)
        new = copy(self.head)
        new.update(new_head_coordinates.to_tuple(), self.head.size)
        self._rects.insert(0, new)

    def collides_with_self(self):
        head = self.head
        return any(body_part.colliderect(head) for body_part in self.tail)

    def found_food(self, snake_food: "SnakeFood") -> bool:
        head = self.head
        LOGGER.debug("Snake found snake food: %s", snake_food)
        return any(head.colliderect(rect) for rect in snake_food.rects)

    def collides_with_sprite(self, sprite: Sprite) -> bool:
        for self_rect in self.rects:
            for sprite_rect in sprite.rects:
                if self_rect.colliderect(sprite_rect):
                    return True
        else:
            return False

    def contains_top_left(self, top_left: Point) -> bool:
        for rect in self.rects:
            if Point(rect.x, rect.y) == top_left:
                return True

        else:
            return False
