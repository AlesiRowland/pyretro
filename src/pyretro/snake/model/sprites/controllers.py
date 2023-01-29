import abc
import logging
from abc import ABC, abstractmethod
from typing import Iterable, TypeVar

import pygame
from pygame import Surface
from pygame.event import Event

from pyretro.snake.controller.commands.registry import init_command_registry
from pyretro.snake.model import (
    Direction, Snake, SnakeCoordinateFactory, SnakeFood,
    SnakeSettings, Sprite, SnakeSpriteFactory,
)
from pyretro.snake.structs import Point, Size

LOGGER = logging.getLogger(__name__)

T = TypeVar("T", bound="SnakeGameController")


class SnakeController(ABC):
    def __init__(self, sprite_factory):
        self._sprite_factory = sprite_factory

    @abstractmethod
    @property
    def sprites(self): ...
    @abstractmethod
    def draw_sprites_onto(self, surface: Surface): ...
    def update_sprite_coordinates(self): ...
    @abc.abstractmethod
    def handle_input(self, pygame_event: Event): ...

    def handle_inputs(self, pygame_events: Iterable[Event]):
        for event in pygame_events:
            self.handle_input(event)


class SnakeInitController(SnakeController):
    def __init__(self, sprite_factory: SnakeSpriteFactory):
        super().__init__(sprite_factory)
        self._title = self._sprite_factory.create_menu_title()
        self._command_registry = init_command_registry

    @property
    def sprites(self) -> list[Sprite]:
        return [self._title]

    def draw_sprites_onto(self, surface: Surface):
        self._title.draw_onto(surface)

    def handle_input(self, pygame_event: Event):
        if pygame_event.type != pygame.K_s:
            self.reset_background()
        elif pygame_event.type != pygame.K_q:
            ...
        else:
            LOGGER.debug(
                f"No handling for pygame event %s during initialisation.",
                pygame_event
            )


class SnakeGameController(SnakeController):
    def __init__(self, sprite_factory: SnakeSpriteFactory):
        super().__init__(sprite_factory)
        self._current_movement_direction = Direction.UP
        self._snake = sprite_factory.create_snake()
        self._snake_food: list[SnakeFood] = []

    @property
    def sprites(self):
        sprites: list[Sprite] = []
        sprites.extend(self._snake_food)
        sprites.append(self._snake)
        return sprites

    def draw_sprites_onto(self, surface: Surface):
        for sprite in self.sprites:
            sprite.draw_onto(surface)

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
        while self._snake.contains_top_left(top_left_point):
            top_left_point = self._coordinate_factory.new_snake_food_location()
        snake_food = self._sprite_factory.create_snake_food(top_left_point)

        self._snake_food.append(snake_food)
        return self

    def get_movement_coordinates(self) -> Point:
        head = self._snake.head
        if self._current_movement_direction is Direction.UP:
            return self._coordinate_factory.get_move_up_coordinates(head)
        if self._current_movement_direction is Direction.DOWN:
            return self._coordinate_factory.get_move_down_coordinates(head)
        if self._current_movement_direction is Direction.RIGHT:
            return self._coordinate_factory.get_move_right_coordinates(head)
        if self._current_movement_direction is Direction.LEFT:
            return self._coordinate_factory.get_move_left_coordinates(head)
        raise TypeError

    def update_sprite_coordinates(self):

        if not self.snake_food:
            self.add_snake_food()

        found_snake_food = self.pop_found_snake_food()
        coordinates = self.get_movement_coordinates()
        if found_snake_food or len(self._snake) < self._snake_settings.auto_grow_until:
            self._snake.grow(coordinates)
        else:
            self._snake.move(coordinates)


#
# class SnakeGameController:
#
#     def __init__(self, snake_settings: SnakeSettings) -> None:
#         self.current_movement_direction = Direction.UP
#         self._snake_settings = snake_settings
#         self._coordinate_factory = SnakeCoordinateFactory(snake_settings)
#         self._sprite_factory = SpriteFactory(self._coordinate_factory)
#
#         self._snake = self._sprite_factory.create_snake()
#         self._snake_food: list[SnakeFood] = []
#
#     @property
#     def snake(self) -> Snake:
#         return self._snake
#
#     @property
#     def screen_size(self) -> Size:
#         return self._coordinate_factory.screen_size
#
#     @property
#     def snake_food(self) -> list[SnakeFood]:
#         return self._snake_food
#
#     @property
#     def sprites(self) -> list[Sprite]:
#         return self._snake_food + [self._snake]  # Always render snake last.
#
#     def pop_found_snake_food(self) -> list[SnakeFood]:
#         remaining_snake_food = []
#         popped_snake_food = []
#         for snake_food in self._snake_food:
#             if self._snake.found_food(snake_food):
#                 popped_snake_food.append(snake_food)
#             else:
#                 remaining_snake_food.append(snake_food)
#         self._snake_food = remaining_snake_food
#         return popped_snake_food
#
#     def add_snake_food(self: T) -> T:
#         top_left_point = self._coordinate_factory.new_snake_food_location()
#         while self._snake.contains_top_left(top_left_point):
#             top_left_point = self._coordinate_factory.new_snake_food_location()
#         snake_food = self._sprite_factory.create_snake_food(top_left_point)
#
#         self._snake_food.append(snake_food)
#         return self
#
#     def get_movement_coordinates(self) -> Point:
#         head = self._snake.head
#         if self.current_movement_direction is Direction.UP:
#             return self._coordinate_factory.get_move_up_coordinates(head)
#         if self.current_movement_direction is Direction.DOWN:
#             return self._coordinate_factory.get_move_down_coordinates(head)
#         if self.current_movement_direction is Direction.RIGHT:
#             return self._coordinate_factory.get_move_right_coordinates(head)
#         if self.current_movement_direction is Direction.LEFT:
#             return self._coordinate_factory.get_move_left_coordinates(head)
#         raise TypeError
#
#     def update_sprite_coordinates(self):
#         if not self.snake_food:
#             self.add_snake_food()
#
#         found_snake_food = self.pop_found_snake_food()
#         coordinates = self.get_movement_coordinates()
#         if found_snake_food or len(self._snake) < self._snake_settings.auto_grow_until:
#             self._snake.grow(coordinates)
#         else:
#             self._snake.move(coordinates)
