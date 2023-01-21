from dataclasses import dataclass

from snake.model.structs import Size


@dataclass
class SnakeSettings:
    unit_size: Size
    grid_size: Size

