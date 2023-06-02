import pytest

from pyretro.langtons_ant.enums import Direction
from pyretro.langtons_ant.ant import Ant, Coordinates


@pytest.mark.unit()
class TestAnt:
    def test_rotate_left_over_bound(self):
        ant = Ant()
        ant.rotate_left()

        result = ant.direction
        assert result == Direction.LEFT

    def test_rotate_right(self):
        ant_direction = Ant()
        ant_direction.rotate_right()

        result = ant_direction.direction
        assert result == Direction.RIGHT

    def test_rotate_right_over_bound(self):
        ant_direction = Ant(direction=Direction.LEFT)
        ant_direction.rotate_right()
        result = ant_direction.direction
        assert result == Direction.UP

    def test_move_up(self):
        coordinates = Coordinates(0, 0)
        ant = Ant(coordinates)
        ant.move()
        expected = Coordinates(0, -1)
        result = ant.coordinates
        assert result == expected

    def test_move_right(self):
        coordinates = Coordinates(0, 0)
        ant = Ant(coordinates, Direction.RIGHT)
        ant.move()
        expected = Coordinates(1, 0)
        result = ant.coordinates
        assert result == expected

    def test_move_down(self):
        coordinates = Coordinates(0, 0)
        ant = Ant(coordinates, Direction.DOWN)
        ant.move()
        expected = Coordinates(0, 1)
        result = ant.coordinates
        assert result == expected

    def test_move_left(self):
        coordinates = Coordinates(0, 0)
        ant = Ant(coordinates, Direction.LEFT)
        ant.move()
        expected = Coordinates(-1, 0)
        result = ant.coordinates
        assert result == expected
