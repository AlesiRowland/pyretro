import logging
from typing import Any, Protocol, TypeVar

import pygame.event

CYCLE_EVENT = pygame.event.custom_type()  # Dictates the cycle of the game.
COLLIDE_EVENT = pygame.event.custom_type()  # Indicates the snake collided.


LOGGER = logging.getLogger(__name__)

T = TypeVar("T", bound="WrappedEvent")


class WrappedEvent(Protocol):
    event: pygame.event.Event = NotImplemented

    @property
    def type(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        ...


class EventWrapper:
    __slots__ = ("event",)

    def __init__(self, event):
        self.event = event
        LOGGER.debug("Wrapped event: %s -> %s", event, self)

    @property
    def type(self) -> int:
        return self.event.type

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.event})"


class KeyEvent(EventWrapper, WrappedEvent):
    @property
    def key(self):
        return self.event.key

    def __hash__(self) -> int:
        return hash((self.event.type, self.event.key))


class InternalEvent(EventWrapper, WrappedEvent):

    def __hash__(self) -> int:
        return hash(self.event.type)


def wrap_event(event):
    if hasattr(event, "key"):
        return KeyEvent(event)
    else:
        return InternalEvent(event)
