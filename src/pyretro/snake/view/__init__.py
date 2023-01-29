from typing import Iterable, TypeVar

import pygame

from pyretro.snake.const import BACKGROUND_COLOR, SNAKE_COLORS
from pyretro.snake.model.sprites.types import Sprite

T = TypeVar("T", bound="SnakeGameView")


class SnakeGameView:
    def __init__(self, surface):
        self._surface = surface

    def reset_background(self):
        self._surface.fill(BACKGROUND_COLOR)

    def render_sprite(self: T, sprite: Sprite) -> T:
        sprite.draw_onto(self._surface)
        return self

    def render_sprites(self: T, sprites: Iterable[Sprite]) -> T:
        for sprite in sprites:
            self.render_sprite(sprite)
        return self

    @staticmethod
    def flip() -> None:
        pygame.display.flip()
