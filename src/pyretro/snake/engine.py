import logging

import pygame.event

from pyretro.snake.state import MenuState
from pyretro.snake.structs import GameSettings

LOGGER = logging.getLogger(__name__)


class SnakeEngine:
    def __init__(self, surface: pygame.Surface, game_settings: GameSettings) -> None:
        pygame.init()

        self.surface = surface
        self.state = MenuState(self, game_settings)
        self.active = False

    def process_events(self) -> None:
        for event in pygame.event.get():
            LOGGER.debug("Handling event: %s", event)
            self.state.handle_event(event)

    def run(self) -> None:
        self.active = True

        while self.active:
            self.process_events()
            self.state.render_sprites(surface=self.surface)
            pygame.display.flip()
