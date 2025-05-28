import pygame

from utils.button import Button
from utils.ui import UI


class Polution:
    def __init__(self) -> None:
        self.generate_button = Button("assets/graphics/polution_report.png", (800, 750))
        self.ui = UI()

    def handle_events(self, ev: pygame.event.Event):
        self.ui.handle_events(ev)

    def render(self, w: pygame.surface.Surface):
        self.generate_button.render(w)
        self.ui.render(w)
