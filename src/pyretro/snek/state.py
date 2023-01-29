import logging
from abc import ABC, abstractmethod
import sys

from typing import Protocol, TypeVar

import pygame
from pygame.event import Event

from .enumerations import Direction
from .events import COLLIDE_EVENT, CYCLE_EVENT
from .sprites import Snake, SnakeFood, Sprite
from .structs import GameSettings, Point, Size
from .factories import SnakeCoordinateFactory, SnakeSpriteFactory

LOGGER = logging.getLogger(__name__)

T = TypeVar("T")


class Engine(Protocol):
    state: "State"
    active: bool


class State(ABC):
    def __init__(self, owner_engine: Engine, game_settings: GameSettings) -> None:
        self._engine = owner_engine
        self._game_settings = game_settings
        unit_size, grid_size = game_settings.unit_size, game_settings.grid_size
        self._coordinate_factory = SnakeCoordinateFactory(unit_size, grid_size)
        self._sprite_factory = SnakeSpriteFactory(self._coordinate_factory)

    @abstractmethod
    def handle_event(self, event: Event) -> None: ...

    @abstractmethod
    def render_sprites(self, surface) -> None: ...


class MenuState(State):
    def __init__(self, owner_engine: Engine, game_settings: GameSettings) -> None:
        super().__init__(owner_engine, game_settings)
        self._title = self._sprite_factory.create_menu_title()

    def handle_event(self, event: Event) -> None:
        if not hasattr(event, "key"):
            return
        if event.key == pygame.K_s:  # todo- think about validation.
            self._engine.state = GameState(self._engine, self._game_settings)
        elif event.key == pygame.K_q:
            self._engine.active = False
        else:
            LOGGER.debug("Invalid event unhandled %s for menu state.", event)

    def render_sprites(self, surface: pygame.Surface) -> None:
        surface.fill(self._game_settings.menu_background_color)
        self._title.draw_onto(surface)


class GameState(State):
    _snake = NotImplemented
    _snake_food = NotImplemented
    _food = NotImplemented
    _current_direction = NotImplemented

    def reset(self) -> None:
        self._snake = self._sprite_factory.create_snake(self._game_settings.block_colors)
        location = self._coordinate_factory.new_snake_food_location()
        self._snake_food = [self._sprite_factory.create_snake_food(location)]
        self._current_direction = Direction.UP
        pygame.event.set_allowed([pygame.KEYDOWN, CYCLE_EVENT])
        pygame.time.set_timer(pygame.event.Event(CYCLE_EVENT), 300)

    def __init__(self,  engine: Engine, game_settings: GameSettings) -> None:
        super().__init__(engine, game_settings)
        self.reset()

    def change_state(self, new_state: State):
        self._engine.state = new_state

    def handle_event(self, event: Event) -> None:

        if event.type == CYCLE_EVENT:
            self.update_sprites()
            return
        elif event.type == COLLIDE_EVENT:
            self._engine.state = GameOverState(self._engine, self._game_settings, len(self._snake))
            return
        elif not hasattr(event, "key"):
            return

        if event.key == pygame.K_q:  # todo- strike 2
            self._engine.active = False
        elif event.key == pygame.K_m:
            self._engine.state = MenuState(self._engine, self._game_settings)
        elif event.key == pygame.K_r:
            self._engine.state = GameState(self._engine, self._game_settings)
        elif event.key == pygame.K_UP:
            self._current_direction = Direction.UP
        elif event.key == pygame.K_DOWN:
            self._current_direction = Direction.DOWN
        elif event.key == pygame.K_RIGHT:
            self._current_direction = Direction.RIGHT
        elif event.key == pygame.K_LEFT:
            self._current_direction = Direction.LEFT
        else:
            LOGGER.debug("Invalid event unhandled %s for game state.", event)

    @property
    def snake(self) -> Snake:
        return self._snake

    @property
    def screen_size(self) -> Size:
        return self._coordinate_factory.screen_size

    @property
    def snake_food(self) -> list[SnakeFood]:
        return self._snake_food

    @property
    def sprites(self) -> list[Sprite]:
        return self._snake_food + [self._snake]  # Always render snake last.

    def pop_found_snake_food(self) -> list[SnakeFood]:
        remaining_snake_food = []
        popped_snake_food = []
        for snake_food in self._snake_food:
            if self._snake.found_food(snake_food):
                popped_snake_food.append(snake_food)
            else:
                remaining_snake_food.append(snake_food)
        self._snake_food = remaining_snake_food
        return popped_snake_food

    def add_snake_food(self: T) -> T:
        top_left_point = self._coordinate_factory.new_snake_food_location()
        snake_food = self._sprite_factory.create_snake_food(top_left_point)
        while self._snake.collides_with_sprite(snake_food):
            top_left_point = self._coordinate_factory.new_snake_food_location()
            snake_food = self._sprite_factory.create_snake_food(top_left_point)

        self.snake_food.append(snake_food)
        return self

    def get_movement_coordinates(self) -> Point:
        head = self._snake.head
        if self._current_direction is Direction.UP:
            return self._coordinate_factory.get_move_up_coordinates(head)
        if self._current_direction is Direction.DOWN:
            return self._coordinate_factory.get_move_down_coordinates(head)
        if self._current_direction is Direction.RIGHT:
            return self._coordinate_factory.get_move_right_coordinates(head)
        if self._current_direction is Direction.LEFT:
            return self._coordinate_factory.get_move_left_coordinates(head)
        raise TypeError

    def update_sprites(self) -> None:
        if not self.snake_food:
            self.add_snake_food()

        found_snake_food = self.pop_found_snake_food()
        coordinates = self.get_movement_coordinates()
        if found_snake_food or len(self._snake) < self._game_settings.auto_grow_until:
            self._snake.grow(coordinates)
        else:
            self._snake.move(coordinates)

        if self._snake.collides_with_self():
            pygame.event.post(Event(COLLIDE_EVENT))

    def render_sprites(self, surface: pygame.Surface) -> None:
        surface.fill(self._game_settings.game_background_color)
        for sprite in self.sprites:
            sprite.draw_onto(surface)


class GameOverState(State):
    def __init__(
            self,
            owner_engine: Engine,
            game_settings: GameSettings,
            score: int
    ) -> None:
        super().__init__(owner_engine, game_settings)
        self._game_over_title = self._sprite_factory.create_game_over_title(score)
        pygame.event.set_allowed([pygame.KEYDOWN, CYCLE_EVENT])
        pygame.time.set_timer(pygame.event.Event(CYCLE_EVENT), 0)

    def handle_event(self, event: Event) -> None:
        if not hasattr(event, "key"):
            return
        if event.key == pygame.K_q:
            self._engine.active = False
        elif event.key == pygame.K_r:
            self._engine.state = GameState(self._engine, self._game_settings)
        elif event.key == pygame.K_m:
            self._engine.state = MenuState(self._engine, self._game_settings)

    def render_sprites(self, surface: pygame.Surface) -> None:
        self._game_over_title.draw_onto(surface)