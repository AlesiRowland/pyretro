from typing import Iterable, TypeVar

import pygame

from snake.const import BACKGROUND_COLOR, SNAKE_COLORS
from snake.model.sprites.types import Sprite

T = TypeVar("T", bound="SnakeGameView")


class SnakeGameView:
    def __init__(self, surface):
        self._surface = surface

    def reset_background(self):
        self._surface.fill(BACKGROUND_COLOR)

    def render_sprite(self: T, sprite: Sprite) -> T:
        for elem in sprite.rects:
            pygame.draw.rect(self._surface, sprite.color, elem)
            pygame.draw.rect(self._surface, SNAKE_COLORS.border, elem, width=1)
        return self

    def render_sprites(self: T, sprites: Iterable[Sprite]) -> T:
        for sprite in sprites:
            self.render_sprite(sprite)
        return self

    @staticmethod
    def flip() -> None:
        pygame.display.flip()
