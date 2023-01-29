from dataclasses import dataclass

from pyretro.snake.structs import Size


@dataclass
class GameSettings:
    unit_size: Size
    grid_size: Size
    menu_background_color: str
    auto_grow_until: int = 10