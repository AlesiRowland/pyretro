import pygame.event

from pyretro.snek.events import CYCLE_EVENT
from pyretro.snek.state import MenuState
from pyretro.snek.structs import GameSettings


class SnakeEngine:
    def __init__(self, surface: pygame.Surface, game_settings: GameSettings) -> None:
        self.surface = surface
        pygame.init()
        self.state = MenuState(self, game_settings)
        self.active = False

    def process_events(self) -> None:
        for event in pygame.event.get():
            self.state.handle_event(event)

    def run(self) -> None:
        self.active = True
        while self.active:
            self.process_events()
            self.state.render_sprites(surface=self.surface)
            pygame.display.flip()
