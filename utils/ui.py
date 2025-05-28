import pygame

from utils.button import Button
from utils.palette import *
from utils.states import State


class UI:
    def __init__(self):
        self.font = pygame.font.Font("assets/fonts/Helvetica.ttf", 32)

        self.buttons = [
            Button("assets/graphics/logo.png", (20, 20)),
            Button("assets/graphics/water_level.png", (20, 220)),
            Button("assets/graphics/polution_level.png", (20, 418)),
            Button("assets/graphics/temperature_level.png", (20, 619)),
        ]

        self.water_text_surface = self.font.render(
            "Poziom wód", True, blue_text_color, None
        )
        self.water_text_rectangle = self.water_text_surface.get_rect(topleft=(220, 300))

        self.title_surface = pygame.image.load("assets/graphics/title.png")
        self.title_rectangle = self.title_surface.get_rect(topleft=(300, 20))

        self.state = State()

    def handle_events(self, ev: pygame.event.Event):
        if self.buttons[0].is_clicked(ev):
            self.state.change_state("MAIN_MENU")
        elif self.buttons[1].is_clicked(ev):
            self.state.change_state("WATER")
        elif self.buttons[2].is_clicked(ev):
            self.state.change_state("POLUTION")
        elif self.buttons[3].is_clicked(ev):
            self.state.change_state("TEMPERATURE")

    def render(self, w: pygame.Surface):
        self.title_surface = self.title_surface.convert_alpha()

        w.blit(self.title_surface, self.title_rectangle)

        w.blit(self.water_text_surface, self.water_text_rectangle)

        for button in self.buttons:
            button.render(w)
