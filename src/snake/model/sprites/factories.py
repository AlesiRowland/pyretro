import random

from snake.model.structs import Size
from snake.model.sprites.rect import SnakeRect
from snake.model.settings import SnakeSettings
from snake.model.sprites.types import Snake, SnakeFood
from snake.model.structs import Point


class SnakeCoordinateFactory:
    def __init__(self, snake_settings: SnakeSettings):
        self.settings = snake_settings

    @property
    def unit_size(self):
        return self.settings.unit_size

    @property
    def screen_size(self):
        return self.settings.unit_size * self.settings.grid_size

    @property
    def player_init_pos(self) -> Point:
        settings = self.settings
        x = settings.unit_size.width * (settings.grid_size.width // 2)
        y = settings.unit_size.height * (settings.grid_size.height // 2)
        return Point(x, y)

    def new_snake_food_location(self) -> Point:
        grid_size = self.settings.grid_size
        rand_x = random.randint(0, grid_size.width)
        rand_y = random.randint(0, grid_size.height)
        x = rand_x * self.settings.unit_size.width
        y = rand_y * self.settings.unit_size.height
        return Point(x, y)

    def get_move_left_coordinates(self, snake_rect: SnakeRect) -> Point:
        x = (snake_rect.x - snake_rect.width) % self.screen_size.width
        return Point(x, snake_rect.y)

    def get_move_right_coordinates(self, snake_rect: SnakeRect) -> Point:
        x = (snake_rect.x + snake_rect.width) % self.screen_size.width
        return Point(x, snake_rect.y)

    def get_move_up_coordinates(self, snake_rect: SnakeRect) -> Point:
        y = (snake_rect.y - snake_rect.height) % self.screen_size.height
        return Point(snake_rect.x, y)

    def get_move_down_coordinates(self, snake_rect: SnakeRect) -> Point:
        y = (snake_rect.y + snake_rect.height) % self.screen_size.height
        return Point(snake_rect.x, y)


class SpriteFactory:
    def __init__(self, coordinate_factory: SnakeCoordinateFactory) -> None:
        self._coordinate_factory = coordinate_factory

    def _create_snake_rect(self, top_left_point: Point) -> SnakeRect:
        unit_size = self._coordinate_factory.unit_size
        return SnakeRect.from_structs(top_left_point, unit_size)

    def create_snake(self) -> Snake:
        top_left_point = self._coordinate_factory.player_init_pos
        snake_head = self._create_snake_rect(top_left_point)
        snake = Snake(snake_head, self._coordinate_factory.screen_size)
        return snake

    def create_snake_food(self, top_left_point: Point) -> SnakeFood:
        snake_rect = self._create_snake_rect(top_left_point)
        snake_food = SnakeFood(snake_rect)
        return snake_food