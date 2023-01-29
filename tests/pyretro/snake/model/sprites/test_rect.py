import pytest
from pytest_cases import fixture

from pyretro.snake.model import Size, SnakeRect


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
