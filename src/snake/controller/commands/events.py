import logging
from typing import Any, Protocol, TypeVar

import pygame

LOGGER = logging.getLogger(__name__)

INTERNAL_EVENT = pygame.event.custom_type()
T = TypeVar("T", bound="WrappedEvent")


class EventWrapper:
    __slots__ = "event",

    def __init__(self, event):
        self.event = event
        LOGGER.debug("Wrapped event: %s -> %s", event, self)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return NotImplemented


class WrappedEvent(Protocol):
    event = NotImplemented

    @property
    def type(self) -> int: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...


class KeyEvent(EventWrapper, WrappedEvent):

    @property
    def key(self):
        return self.event.key

    @property
    def type(self) -> int:
        return self.event.type

    def __hash__(self) -> int:
        return hash((self.event.type, self.event.key))


class InternalEvent(EventWrapper, WrappedEvent):

    @property
    def type(self) -> int:
        return INTERNAL_EVENT

    def __hash__(self) -> int:
        return hash(self.event.type)


def wrap_event(event):
    if hasattr(event, "key"):
        return KeyEvent(event)

    else:
        return InternalEvent(event)