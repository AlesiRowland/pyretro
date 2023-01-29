from abc import ABC, abstractmethod
from collections import defaultdict

import pygame.event

from pyretro.snake.enums import Direction
from pyretro.snake.events import wrap_event


class Subscriber:
    @abstractmethod
    def update(self):
        ...


class StateSubscriber(Subscriber, ABC):
    def __init__(self, state) -> None:
        self._state = state


class GameStateSubscriber(Subscriber, ABC):
    def __init__(self, game_state) -> None:
        self._game_state = game_state


class GameStateSetter(StateSubscriber):
    def update(self):
        self._state.to_game_state()


class MenuStateSetter(StateSubscriber):
    def update(self):
        self._state.to_menu_state()


class QuitSetter(StateSubscriber):
    def update(self):
        self._state._owner_engine.active = False


class GameOverStateSetter(GameStateSubscriber):
    def update(self):
        self._game_state.to_game_over_state()


class DirectionChangeSetter(GameStateSubscriber):
    def __init__(self, direction: Direction, game_state) -> None:
        super().__init__(game_state)
        self._direction = direction

    def update(self):
        self._game_state.change_snake_direction(self._direction)


class SpriteUpdater(GameStateSubscriber):
    def update(self) -> None:
        self._game_state.update_sprites()


class EventHandler:
    def __init__(self, subscribers=None):
        self._subscribers = defaultdict(lambda: [], subscribers or {})

    def add_subscriber(self, key, subscriber):
        self._subscribers[key].append(subscriber)
        return self

    def handle_event(self, event: pygame.event.Event):
        wrapped = wrap_event(event)
        subscribers = self._subscribers[wrapped]
        for subscriber in subscribers:
            subscriber.update()
