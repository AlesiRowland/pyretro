
import pytest
from pytest_cases import fixture

from snake.model.sprites.rect import SnakeRect
from snake.model.structs import Point, Size


@pytest.mark.unit
class TestSnakeRect:

    @fixture
    def snake_rect(self):
        return SnakeRect(0, 0, 50, 50)

    @fixture
    def screen_size(self):
        return Size(100, 100)

    def test_to_tuple(self, snake_rect):
        assert snake_rect.to_tuple() == (0, 0, 50, 50)

    def test_from_structs(self):
        expected = SnakeRect(20, 20, 30, 30)
        actual = SnakeRect.from_structs(Point(20, 20), Size(30, 30))
        assert actual == expected

    def test_get_move_left_coordinates(self, screen_size):
        snake_rect = SnakeRect(50, 50, 20, 20)
        actual = snake_rect.get_move_left_coordinates(screen_size)
        expected = Point(30, 50)
        assert actual == expected

    def test_get_move_left_wrapped_coordinates(self, screen_size):
        snake_rect = SnakeRect(0, 50, 20, 20)
        actual = snake_rect.get_move_left_coordinates(screen_size)
        expected = Point(80, 50)
        assert actual == expected

    def test_get_move_right_coordinates(self, screen_size):
        snake_rect = SnakeRect(70, 50, 20, 20)
        actual = snake_rect.get_move_right_coordinates(screen_size)
        expected = Point(70, 50)
        assert actual == expected

    def test_get_move_right_coordinates(self, screen_size):
        snake_rect = SnakeRect(100, 50, 20, 20)
        actual = snake_rect.get_move_right_coordinates(screen_size)
        expected = Point(20, 50)
        assert actual == expected

    def test_get_move_up_coordinates(self, screen_size):
        snake_rect = SnakeRect(50, 50, 20, 20)
        actual = snake_rect.get_move_up_coordinates(screen_size)
        expected = Point(50, 30)
        assert actual == expected

    def test_get_move_wrapped_up_coordinates(self, screen_size):
        snake_rect = SnakeRect(50, 0, 20, 20)
        actual = snake_rect.get_move_up_coordinates(screen_size)
        expected = Point(50, 80)
        assert actual == expected

    def test_get_move_down_coordinates(self, screen_size):
        snake_rect = SnakeRect(50, 50, 20, 20)
        actual = snake_rect.get_move_down_coordinates(screen_size)
        expected = Point(50, 70)
        assert actual == expected

    def test_get_move_wrapped_down_coordinates(self, screen_size):
        snake_rect = SnakeRect(50, 100, 20, 20)
        actual = snake_rect.get_move_down_coordinates(screen_size)
        expected = Point(50, 20)
        assert actual == expected