import pygame

from utils.button import Button
from utils.palette import *
from utils.states import State


class MainMenu:
    def __init__(self) -> None:
        self.font = pygame.font.Font("assets/fonts/Helvetica.ttf", 32)

        self.logo_surface = pygame.image.load("assets/graphics/logo.png")
        self.logo_rectangle = self.logo_surface.get_rect(topleft=(20, 20))

        self.title_surface = pygame.image.load("assets/graphics/title.png")
        self.title_rectangle = self.title_surface.get_rect(topleft=(300, 20))

        self.buttons = [
            Button("assets/graphics/water_level.png", (20, 220)),
            Button("assets/graphics/polution_level.png", (20, 418)),
            Button("assets/graphics/temperature_level.png", (20, 619)),
            Button("assets/graphics/generate_report.png", (20, 750)),
        ]

        self.water_text_surface = self.font.render(
            "Poziom wód", True, blue_text_color, None
        )
        self.water_text_rectangle = self.water_text_surface.get_rect(topleft=(220, 300))

        self.report_text_surface = self.font.render(
            "Generuj raport", True, blue_text_color, None
        )
        self.report_text_rectangle = self.report_text_surface.get_rect(
            topleft=(220, 750)
        )

        self.state = State()

    def handle_events(self, ev: pygame.event.Event):
        if self.buttons[0].is_clicked(ev):
            self.state.change_state("WATER")
        elif self.buttons[3].is_clicked(ev):
            self.state.change_state("GENERATE_REPORT")

    def render(self, w: pygame.Surface):
        self.logo_surface = self.logo_surface.convert_alpha()
        self.title_surface = self.title_surface.convert_alpha()

        w.blit(self.logo_surface, self.logo_rectangle)
        w.blit(self.title_surface, self.title_rectangle)

        w.blit(self.water_text_surface, self.water_text_rectangle)
        w.blit(self.report_text_surface, self.report_text_rectangle)

        for button in self.buttons:
            button.render(w)
