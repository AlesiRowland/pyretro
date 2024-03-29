from enum import auto, Enum


class SquareColor(Enum):
    WHITE = auto()
    BLACK = auto()


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
