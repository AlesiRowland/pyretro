import pytest
from pytest_cases import fixture

from snake.model import SnakeFood, SnakeRect


@pytest.mark.unit
class TestSnakeFood:
    @fixture
    def snake_food(self) -> SnakeFood:
        return SnakeFood(SnakeRect(20, 20, 20, 20))

    def test_len(self, snake_food: SnakeFood) -> None:
        assert len(snake_food) == 1

    def test_rects_property(self, snake_food: SnakeFood) -> None:
        assert snake_food.rects == [SnakeRect(20, 20, 20, 20)]