from ._base import ControllerCommand
from .events import WrappedEvent


class ControllerCommandRegistry:
    def __init__(self):
        self.__bindings = {}

    def register(self, event: WrappedEvent):
        def decorator(cls):
            self.__bindings[event] = cls

        return decorator

    def is_registered(self, event: WrappedEvent):
        return event in self.__bindings

    def create_command(self, event: WrappedEvent, controller) -> ControllerCommand:
        cls = self.__bindings[event]
        return cls(controller)


command_registry = ControllerCommandRegistry()