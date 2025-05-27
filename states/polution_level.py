import pygame

from utils.ui import UI


class Polution:
    def __init__(self) -> None:
        self.ui = UI()

    def handle_events(self, ev: pygame.event.Event):
        self.ui.handle_events(ev)

    def render(self, w: pygame.surface.Surface):
        self.ui.render(w)
