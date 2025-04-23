import pygame

from utils.palette import *


class MainMenu:
    def __init__(self) -> None:
        self.title_font = pygame.font.Font("assets/fonts/Helvetica.ttf", 64)
        # self.normal_font = pygame.font.Font("../assets/fonts/Helvetica.ttf", 32)

        self.title_surface = self.title_font.render(
            "Hydro mazury", True, dark_text_color, None
        )
        self.title_rectangle = self.title_surface.get_rect(center=(640, 100))

        self.logo_surface = pygame.image.load("assets/graphics/logo.png")
        self.logo_rectangle = self.logo_surface.get_rect(topleft=(20, 20))

    def render(self, w: pygame.Surface):
        w.blit(self.logo_surface, self.logo_rectangle)
        w.blit(self.title_surface, self.title_rectangle)
