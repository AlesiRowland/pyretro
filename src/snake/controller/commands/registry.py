from collections import defaultdict
from collections.abc import Callable
from typing import Type

from .base import ControllerCmd
from .events import WrappedEvent

CmdRegistrationDecorator = Callable[[Type[ControllerCmd], None]]


class ControllerCmdRegistry:
    def __init__(self):
        self._bindings = defaultdict(lambda: [])

    def subscribe(self, event: WrappedEvent) -> CmdRegistrationDecorator:
        def decorator(cls: Type[ControllerCmd]) -> None:
            self._bindings[event].append(cls)

        return decorator

    def has_subscribed_commands(self, event: WrappedEvent) -> bool:
        return event in self._bindings

    def create_subscribed(self, event: WrappedEvent, controller: "SnakeController") -> list[ControllerCmd]:
        return [cls(controller) for cls in self._bindings[event]]


game_command_registry = ControllerCmdRegistry()
init_command_registry = ControllerCmdRegistry()