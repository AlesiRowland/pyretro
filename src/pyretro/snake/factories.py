import random

from .sprites import Snake, SnakeFood, SnakeRect, TitleSprite
from .structs import BlockColors, Point, Size


class SnakeCoordinateFactory:
    def __init__(self, unit_size: Size, grid_n: Size) -> None:
        self.unit_size = unit_size
        self.grid_size = grid_n

    @property
    def screen_size(self) -> Size:
        return self.unit_size * self.grid_size

    @property
    def center_pos(self) -> Point:
        x = self.unit_size.width * (self.grid_size.width // 2)
        y = self.unit_size.height * (self.grid_size.height // 2)
        return Point(x, y)

    def new_snake_food_location(self) -> Point:
        rand_x = random.randint(0, self.grid_size.width - 1)
        rand_y = random.randint(0, self.grid_size.height - 1)
        x = rand_x * self.unit_size.width
        y = rand_y * self.unit_size.height
        return Point(x, y)

    def get_center(self) -> int:
        return self.screen_size // 2

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


class SnakeSpriteFactory:
    def __init__(self, coordinate_factory: SnakeCoordinateFactory) -> None:
        self._coordinate_factory = coordinate_factory

    def _create_snake_rect(self, top_left_point: Point) -> SnakeRect:
        unit_size = self._coordinate_factory.unit_size
        return SnakeRect.from_structs(top_left_point, unit_size)

    def create_snake(self, colors: BlockColors) -> Snake:
        top_left_point = self._coordinate_factory.center_pos
        snake_head = self._create_snake_rect(top_left_point)
        snake = Snake(snake_head, self._coordinate_factory.screen_size, colors)
        return snake

    def create_snake_food(self, top_left: Point, colors: BlockColors) -> SnakeFood:
        snake_rect = self._create_snake_rect(top_left)
        snake_food = SnakeFood(snake_rect, colors)
        return snake_food

    def create_menu_title(self) -> TitleSprite:
        pos = self._coordinate_factory.center_pos
        title = TitleSprite("Snake", pos, "purple")
        return title

    def create_game_over_title(self, score: int) -> TitleSprite:
        pos = self._coordinate_factory.center_pos
        title = TitleSprite(f"Game Over! Score: {score}", pos)
        return title