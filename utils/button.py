import pygame


class Button:
    def __init__(self, path: str, position: tuple[int, int]) -> None:
        self.surface = pygame.image.load(path)
        self.rect = self.surface.get_rect(topleft=position)

    def is_clicked(self, ev: pygame.event.Event):
        return (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and ev.type == pygame.MOUSEBUTTONUP
        )

    def render(self, w: pygame.Surface):
        w.blit(self.surface, self.rect)
