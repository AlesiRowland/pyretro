import logging
from collections.abc import Iterable

import pygame
from pygame.event import Event  # type: ignore

from pyretro.snake.model import SnakeGameModel
from pyretro.snake.view import SnakeGameView
from .commands import game_command_registry
from .commands.events import INTERNAL_EVENT, wrap_event

LOGGER = logging.getLogger(__name__)


class SnakeGameController:
    def __init__(self, snake_model: SnakeGameModel, snake_view: SnakeGameView):
        self.snake_model = snake_model
        self.snake_view = snake_view
        self._commands = game_command_registry
        self._is_running = False
        self._is_paused = False
        pygame.event.set_allowed([pygame.KEYDOWN, INTERNAL_EVENT])
        pygame.time.set_timer(Event(INTERNAL_EVENT), 500)

    def process_events(self, events: Iterable[Event]) -> None:
        for event in events:
            LOGGER.debug("processing %s", event)
            wrapped = wrap_event(event)
            LOGGER.debug("Wrapped %s -> %s", event, wrapped)
            for command in self._commands.create_subscribed(wrapped, self):
                LOGGER.debug("Executing command: %s", type(command).__name__)
                command.execute()

    def run(self):
        self._is_running = True

        while self._is_running:
            self.process_events(pygame.event.get())
            self.snake_view.reset_background()
            self.snake_view.render_sprites(self.snake_model.sprites)
            self.snake_view.flip()

    def alter_direction(self, direction):
        self.snake_model.current_movement_direction = direction

    def update_coordinates(self):
        self.snake_model.update_sprite_coordinates()