import sys

import pygame
from pygame.event import Event

from .base import ControllerCmd
from .events import INTERNAL_EVENT, InternalEvent, KeyEvent
from .registry import game_command_registry
from pyretro.snake.model.enums import Direction


class SetDirection(ControllerCmd):
    direction: Direction = NotImplemented

    def execute(self):
        self._controller.alter_direction(self.direction)


@game_command_registry.subscribe(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_UP)))
class SetDirectionUp(SetDirection):
    direction = Direction.UP


@game_command_registry.subscribe(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_DOWN)))
class SetDirectionDown(SetDirection):
    direction = Direction.DOWN


@game_command_registry.subscribe(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_RIGHT)))
class SetDirectionRight(SetDirection):
    direction = Direction.RIGHT


@game_command_registry.subscribe(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_LEFT)))
class SetDirectionLeft(SetDirection):
    direction = Direction.LEFT


@game_command_registry.subscribe(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_q)))
class QuitCmd(ControllerCmd):
    def execute(self):
        sys.exit(0)


@game_command_registry.subscribe(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_SPACE)))
class PauseCmd(ControllerCmd):
    def execute(self) -> None:
        self._controller.is_paused = not self._controller.is_paused


@game_command_registry.subscribe(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_r)))
class RestartCmd(ControllerCmd):
    def execute(self) -> None:
        self._controller.restart()


@game_command_registry.subscribe(InternalEvent(Event(INTERNAL_EVENT)))
class MoveSnake(ControllerCmd):
    def execute(self):
        self._controller.update_coordinates()