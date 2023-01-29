import abc
import logging
from copy import copy
from typing import Type, TypeVar

import pygame

from pyretro.snake.structs import Point, Size
from pyretro.snake.structs import BlockColors

Self = TypeVar("Self", bound="SnakeRect")

LOGGER = logging.getLogger(__name__)


class SnakeRect(pygame.Rect):
    """Represents a rect for the Snake Game."""

    def to_tuple(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.width, self.height

    @classmethod
    def from_structs(cls: Type[Self], point: Point, size: Size) -> Self:
        return cls(point.x, point.y, size.width, size.height)


class Sprite(abc.ABC):
    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.rects == other.rects

    @property
    @abc.abstractmethod
    def rects(self):
        ...

    @abc.abstractmethod
    def draw_onto(self, surface):
        ...


class TitleSprite(Sprite):
    def __init__(self, text, center, color="black", size=24):
        font = pygame.font.SysFont("arialunicode", size, True, False)
        self._text = font.render(text, True, color)
        self._rect = self._text.get_rect(center=center.to_tuple())

    @property
    def rects(self):
        return [self._rect]

    def draw_onto(self, surface):
        surface.blit(self._text, self._rect)


class SnakeFood(Sprite):
    def __init__(self, snake_rect: SnakeRect, colors: BlockColors) -> None:
        self._rect = snake_rect
        self.colors = colors

    @property
    def rects(self) -> list[SnakeRect]:
        return [self._rect]

    def __str__(self):
        return f"{type(self).__name__}({self._rect})"

    def draw_onto(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.colors.fill, self._rect)
        pygame.draw.rect(surface, self.colors.border, self._rect, width=1)


class Snake(Sprite):
    def __init__(self, head: SnakeRect, screen_size: Size, colors: BlockColors) -> None:
        self._rects = [head]
        self._screen_size = screen_size
        self._colors = colors

    def __len__(self) -> int:
        return len(self._rects)

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

    def collides_with_self(self) -> bool:
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

    def draw_onto(self, surface: pygame.Surface) -> None:
        for rect in self.rects:
            pygame.draw.rect(surface, self._colors.fill, rect)
            pygame.draw.rect(surface, self._colors.border, rect, width=1)
