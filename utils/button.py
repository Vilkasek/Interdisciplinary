import pygame


class Button:
    def __init__(self, path: str, position: tuple[int, int]) -> None:
        self.surface = pygame.image.load(path)
        self.rect = self.surface.get_rect(topleft=position)

    def render(self, w: pygame.Surface):
        w.blit(self.surface, self.rect)
