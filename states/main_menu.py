import pygame

from utils.palette import *


class MainMenu:
    def __init__(self) -> None:
        self.logo_surface = pygame.image.load("assets/graphics/logo.png")
        self.logo_rectangle = self.logo_surface.get_rect(topleft=(20, 20))

        self.title_surface = pygame.image.load("assets/graphics/title.png")
        self.title_rectangle = self.title_surface.get_rect(topleft=(300, 20))

    def render(self, w: pygame.Surface):
        w.blit(self.logo_surface, self.logo_rectangle)
        w.blit(self.title_surface, self.title_rectangle)
