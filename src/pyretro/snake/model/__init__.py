from typing import TypeVar

from .enums import Direction
from .settings import SnakeSettings
from .sprites.factories import SpriteFactory, SnakeCoordinateFactory
from .sprites.rect import SnakeRect
from .sprites.types import Snake, SnakeFood, Sprite
from .structs import Point, Size

T = TypeVar("T", bound="SnakeGameModel")


class SnakeGameModel:
    def __init__(self, snake_settings: SnakeSettings) -> None:
        self.current_movement_direction = Direction.UP

        self._coordinate_factory = SnakeCoordinateFactory(snake_settings)
        self._sprite_factory = SpriteFactory(self._coordinate_factory)

        self._snake = self._sprite_factory.create_snake()
        self._snake_food: list[SnakeFood] = []

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
        while self._snake.contains_top_left(top_left_point):
            top_left_point = self._coordinate_factory.new_snake_food_location()
        snake_food = self._sprite_factory.create_snake_food(top_left_point)

        self._snake_food.append(snake_food)
        return self

    def get_movement_coordinates(self) -> Point:
        head = self._snake.head
        if self.current_movement_direction is Direction.UP:
            return self._coordinate_factory.get_move_up_coordinates(head)
        if self.current_movement_direction is Direction.DOWN:
            return self._coordinate_factory.get_move_down_coordinates(head)
        if self.current_movement_direction is Direction.RIGHT:
            return self._coordinate_factory.get_move_right_coordinates(head)
        if self.current_movement_direction is Direction.LEFT:
            return self._coordinate_factory.get_move_left_coordinates(head)
        raise TypeError

    def update_sprite_coordinates(self):
        if not self.snake_food:
            self.add_snake_food()

        found_snake_food = self.pop_found_snake_food()
        coordinates = self.get_movement_coordinates()
        if found_snake_food or len(self._snake) < 10:
            self._snake.grow(coordinates)
        else:
            self._snake.move(coordinates)
