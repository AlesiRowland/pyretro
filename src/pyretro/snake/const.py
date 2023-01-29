from pyretro.snake.structs import BlockColors, GameSettings, Size

DEFAULT_GAME_SETTINGS = GameSettings(
    unit_size=Size(20, 20),
    grid_size=Size(20, 20),
    speed=300,
    snake_colors=BlockColors("purple", "black"),
    snake_food_colors=BlockColors("red", "black"),
    game_background_color="green",
    menu_background_color="green",
    game_over_background_color="green",
)
