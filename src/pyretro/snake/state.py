import logging
from abc import ABC, abstractmethod

from typing import Protocol, TypeVar

import pygame
from pygame.event import Event

from .enums import Direction
from .events import COLLIDE_EVENT, CYCLE_EVENT, InternalEvent, KeyEvent, WrappedEvent
from .pubsub import (
    DirectionChangeSetter, EventHandler, GameOverStateSetter,
    GameStateSetter, MenuStateSetter, QuitSetter, SpriteUpdater, StateSubscriber,
)
from .sprites import Snake, SnakeFood, Sprite
from .structs import GameSettings, Point, Size
from .factories import SnakeCoordinateFactory, SnakeSpriteFactory

LOGGER = logging.getLogger(__name__)

T = TypeVar("T")


class Engine(Protocol):
    state: "State"
    active: bool


class State(ABC):
    def __init__(self, owner_engine: Engine, game_settings: GameSettings) -> None:
        pygame.event.set_blocked(None)
        self.owner_engine = owner_engine
        self.game_settings = game_settings
        unit_size, grid_size = game_settings.unit_size, game_settings.grid_size
        self._coordinate_factory = SnakeCoordinateFactory(unit_size, grid_size)
        self._sprite_factory = SnakeSpriteFactory(self._coordinate_factory)

    @classmethod
    def name(cls):
        return cls.__name__

    @abstractmethod
    def handle_event(self, event: Event) -> None: ...

    @abstractmethod
    def render_sprites(self, surface) -> None: ...

    def change_state(self, new_state: 'State'):
        LOGGER.debug("Changing State: %s -> %s", self.name, new_state.name)
        self.owner_engine.state = new_state

    def to_game_state(self):
        game_state = GameState(self.owner_engine, self.game_settings)
        self.change_state(game_state)
        LOGGER.debug("Changed state %s -> %s", self.name, game_state.name)

    def to_menu_state(self):
        menu_state = MenuState(self.owner_engine, self.game_settings)
        self.change_state(menu_state)
        LOGGER.debug("Changed state %s -> %s", self.name, menu_state.name)


class MenuState(State):
    def __init__(self, owner_engine: Engine, game_settings: GameSettings) -> None:
        super().__init__(owner_engine, game_settings)
        self._title = self._sprite_factory.create_menu_title()
        subscriber_bindings: dict[WrappedEvent: list[StateSubscriber]] = {
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_m)): [MenuStateSetter(self)],
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_s)): [GameStateSetter(self)],
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_q)): [QuitSetter(self)],
        }
        self._event_handler = EventHandler(subscriber_bindings)
        pygame.event.set_allowed(pygame.KEYDOWN)

    def handle_event(self, event: Event) -> None:
        self._event_handler.handle_event(event)

    def render_sprites(self, surface: pygame.Surface) -> None:
        surface.fill(self.game_settings.menu_background_color)
        self._title.draw_onto(surface)


class GameState(State):
    _snake = NotImplemented
    _snake_food = NotImplemented
    _food = NotImplemented
    _current_direction = NotImplemented

    def __init__(self,  engine: Engine, game_settings: GameSettings) -> None:
        super().__init__(engine, game_settings)
        subscriber_bindings: dict[WrappedEvent: list[StateSubscriber]] = {
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_UP)): [DirectionChangeSetter(Direction.UP, self)],
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_DOWN)): [DirectionChangeSetter(Direction.DOWN, self)],
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_RIGHT)): [DirectionChangeSetter(Direction.RIGHT, self)],
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_LEFT)): [DirectionChangeSetter(Direction.LEFT, self)],
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_m)): [MenuStateSetter(self)],
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_r)): [GameStateSetter(self)],
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_q)): [QuitSetter(self)],
            InternalEvent(Event(CYCLE_EVENT)): [SpriteUpdater(self)],
            InternalEvent(Event(COLLIDE_EVENT)): [GameOverStateSetter(self)],

        }
        self._event_handler = EventHandler(subscriber_bindings)
        self._snake = self._sprite_factory.create_snake(self.game_settings.snake_colors)
        location = self._coordinate_factory.new_snake_food_location()
        self._snake_food = [self._sprite_factory.create_snake_food(location, self.game_settings.snake_food_colors)]
        self._current_direction = Direction.UP
        self._snake_moved = False
        pygame.event.set_allowed([pygame.KEYDOWN, CYCLE_EVENT])
        pygame.time.set_timer(pygame.event.Event(CYCLE_EVENT), 300)

    @property
    def current_score(self):
        return len(self._snake)

    def change_snake_direction(self, direction: Direction) -> None:

        if self._snake_moved:
            return
        self._current_direction = direction
        self._snake_moved = True

    def handle_event(self, event: Event) -> None:
        self._event_handler.handle_event(event)

    @property
    def snake(self) -> Snake:
        return self._snake

    @property
    def screen_size(self) -> Size:
        return self._coordinate_factory.screen_size

    @property
    def snake_food(self) -> list[SnakeFood]:
        return self._snake_food

    @property
    def sprites(self) -> list[Sprite]:
        return self._snake_food + [self._snake]  # Always render snake last.

    def pop_found_snake_food(self) -> list[SnakeFood]:
        remaining_snake_food = []
        popped_snake_food = []
        for snake_food in self._snake_food:
            if self._snake.found_food(snake_food):
                popped_snake_food.append(snake_food)
            else:
                remaining_snake_food.append(snake_food)
        self._snake_food = remaining_snake_food
        return popped_snake_food

    def add_snake_food(self: T) -> T:
        top_left_point = self._coordinate_factory.new_snake_food_location()
        colors = self.game_settings.snake_food_colors
        snake_food = self._sprite_factory.create_snake_food(top_left_point, colors)
        while self._snake.collides_with_sprite(snake_food):
            top_left_point = self._coordinate_factory.new_snake_food_location()
            snake_food = self._sprite_factory.create_snake_food(top_left_point, colors)

        self.snake_food.append(snake_food)
        return self

    def get_movement_coordinates(self) -> Point:
        head = self._snake.head
        if self._current_direction is Direction.UP:
            return self._coordinate_factory.get_move_up_coordinates(head)
        if self._current_direction is Direction.DOWN:
            return self._coordinate_factory.get_move_down_coordinates(head)
        if self._current_direction is Direction.RIGHT:
            return self._coordinate_factory.get_move_right_coordinates(head)
        if self._current_direction is Direction.LEFT:
            return self._coordinate_factory.get_move_left_coordinates(head)
        raise TypeError

    def update_sprites(self) -> None:
        if not self.snake_food:
            self.add_snake_food()

        found_snake_food = self.pop_found_snake_food()
        coordinates = self.get_movement_coordinates()
        auto_grow_until = self.game_settings.auto_grow_until
        if found_snake_food or len(self.snake) < auto_grow_until:
            self.snake.grow(coordinates)
        else:
            self.snake.move(coordinates)

        if self.snake.collides_with_self():
            LOGGER.debug("Snake Collided with itself")
            pygame.event.post(pygame.event.Event(COLLIDE_EVENT))
        self._snake_moved = False

    def render_sprites(self, surface: pygame.Surface) -> None:
        surface.fill(self.game_settings.game_background_color)
        for sprite in self.sprites:
            sprite.draw_onto(surface)

    def to_game_over_state(self):
        game_over_state = GameOverState(self.owner_engine,
                                        self.game_settings,
                                        self.current_score
                                        )
        self.change_state(game_over_state)
        LOGGER.debug("Changed state %s -> %s", self.name, game_over_state.name)


class GameOverState(State):
    def __init__(
            self,
            owner_engine: Engine,
            game_settings: GameSettings,
            score: int,
    ) -> None:
        super().__init__(owner_engine, game_settings)
        self._game_over_title = self._sprite_factory.create_game_over_title(score)
        pygame.event.set_allowed([pygame.KEYDOWN, CYCLE_EVENT])
        pygame.time.set_timer(pygame.event.Event(CYCLE_EVENT), 0)
        subscriber_bindings: dict[WrappedEvent: list[StateSubscriber]] = {
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_m)): [MenuStateSetter(self)],
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_r)): [GameStateSetter(self)],
            KeyEvent(Event(pygame.KEYDOWN, key=pygame.K_q)): [QuitSetter(self)],
        }
        self._event_handler = EventHandler(subscriber_bindings)

    def handle_event(self, event: Event) -> None:
        self._event_handler.handle_event(event)

    def render_sprites(self, surface: pygame.Surface) -> None:
        self._game_over_title.draw_onto(surface)