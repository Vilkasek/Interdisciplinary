import os
import sys

import matplotlib
import pygame

matplotlib.use("Agg")

from states.main_menu import MainMenu
from states.polution_level import Polution
from states.temperature_level import Temperature
from states.water_level import Water
from utils.palette import *
from utils.states import State


class App:
    def __init__(self) -> None:
        pygame.init()

        self.WIDTH, self.HEIGHT = 1600, 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Hydro Mazury")

        self.clock = pygame.time.Clock()
        self.running: bool = True

        self.state = State()

        os.makedirs("assets/data", exist_ok=True)
        os.makedirs("reports", exist_ok=True)

        self.main_menu = MainMenu()
        self.water_menu = Water()
        self.polution_menu = Polution()
        self.temperature_menu = Temperature()

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

            match self.state.state:
                case "MAIN_MENU":
                    self.main_menu.handle_events(event)
                case "WATER":
                    self.water_menu.handle_events(event)
                case "POLUTION":
                    self.polution_menu.handle_events(event)
                case "TEMPERATURE":
                    self.temperature_menu.handle_events(event)

    def update(self) -> None:
        match self.state.state:
            case "MAIN_MENU":
                pass
            case "WATER":
                pass
            case "POLUTION":
                pass
            case "TEMPERATURE":
                pass

    def render(self) -> None:
        self.screen.fill(background_color)

        match self.state.state:
            case "MAIN_MENU":
                self.main_menu.render(self.screen)
            case "WATER":
                self.water_menu.render(self.screen)
            case "POLUTION":
                self.polution_menu.render(self.screen)
            case "TEMPERATURE":
                self.temperature_menu.render(self.screen)

        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = App()
    app.run()
