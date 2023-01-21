import sys

import pygame
from pygame.event import Event

from ._base import ControllerCommand
from .events import INTERNAL_EVENT, InternalEvent, KeyEvent
from .registry import command_registry
from snake.model.enums import Direction


class SetDirection(ControllerCommand):
    direction = NotImplemented

    def execute(self):
        self._controller.alter_direction(self.direction)


@command_registry.register(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_UP)))
class SetDirectionUp(SetDirection):
    direction = Direction.UP


@command_registry.register(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_DOWN)))
class SetDirectionDown(SetDirection):
    direction = Direction.DOWN


@command_registry.register(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_RIGHT)))
class SetDirectionRight(SetDirection):
    direction = Direction.RIGHT


@command_registry.register(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_LEFT)))
class SetDirectionLeft(SetDirection):
    direction = Direction.LEFT


@command_registry.register(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_q)))
class QuitCommand(ControllerCommand):
    def execute(self):
        sys.exit(0)


@command_registry.register(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_SPACE)))
class PauseCommand(ControllerCommand):
    def execute(self) -> None:
        self._controller.is_paused = not self._controller.is_paused


@command_registry.register(KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_r)))
class RestartCommand(ControllerCommand):
    def execute(self) -> None:
        self._controller.restart()


@command_registry.register(InternalEvent(Event(INTERNAL_EVENT)))
class MoveSnake(ControllerCommand):
    def execute(self):
        self._controller.update_coordinates()