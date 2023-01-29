import dataclasses
import logging
from abc import ABC, abstractmethod
import sys

from typing import Protocol

import pygame
from pygame.event import Event

from pyretro.snake.model import SnakeCoordinateFactory, SnakeSpriteFactory
from pyretro.snake.model.settings import GameSettings
from pyretro.snake.structs import Size

LOGGER = logging.getLogger(__name__)


class StateOwner(Protocol):
    state: "State"



class State(ABC):
    @abstractmethod
    def handle_input(self, owner: StateOwner, event: Event) -> None: ...

    def update_sprites(self) -> None: ...

    @abstractmethod
    def render_sprites(self, surface) -> None: ...


class MenuState(State):
    def __init__(self, game_settings: GameSettings):
        self._game_settings = game_settings
        coordinate_factory = SnakeCoordinateFactory(
            game_settings.unit_size, game_settings.grid_size
        )
        self._sprite_factory = SnakeSpriteFactory(coordinate_factory)
        self._title = self._sprite_factory.create_menu_title()

    def handle_input(self, owner: StateOwner, event: Event) -> None:
        if event.key == pygame.K_s:  # todo- think about validation.
            owner.state = GameState(self._game_settings)
        elif event.key == pygame.K_q:
            sys.exit(0)
        else:
            LOGGER.debug("Invalid event unhandled %s for initialisation state.", event)

    def render_sprites(self, surface) -> None:
        surface.fill(self._game_settings.menu_background_color)
        self._title.draw_onto(surface)


class GameState(State):
    def __init__(self, game_settings: GameSettings):
        self._game_settings = game_settings
        coordinate_factory = SnakeCoordinateFactory(game_settings)
        self._sprite_factory = SnakeSpriteFactory(coordinate_factory)

        self._snake = self._sprite_factory.create_snake()
        self._food = self._sprite_factory.create_snake_food()

    def handle_input(self, owner: StateOwner, event: Event) -> None:
        if event.key == pygame.K_q:  # todo- strike 2
            sys.exit(0)

        elif event.key == pygame.K_m:
            owner.state = MenuState(self._game_settings)
        elif event.key == pygame.K_r:

        elif event.key == pygame.K_UP:
