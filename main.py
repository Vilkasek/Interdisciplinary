import sys

import pygame

from states.main_menu import MainMenu
from utils.palette import *
from utils.states import State


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Hydro Mazury")

        self.clock = pygame.time.Clock()
        self.running: bool = True

        self.state = State()

        self.main_menu = MainMenu()

    def run(self) -> None:
        while self.state.running:
            self.handle_events()

            self.update()
            self.render()

            self.clock.tick(60)

        self.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.toggle_run_state(False)

    def update(self) -> None:
        match self.state.state:
            case "MAIN_MENU":
                pass
            case "APP":
                pass

    def render(self) -> None:
        self.screen.fill(background_color)

        match self.state.state:
            case "MAIN_MENU":
                self.main_menu.render(self.screen)
            case "APP":
                pass

        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
