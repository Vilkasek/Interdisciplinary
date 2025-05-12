import os
import sys

import matplotlib
import pygame

matplotlib.use("Agg")  # Non-interactive backend for matplotlib

from data_loader import DataLoader
from pdf_generator import PDFReportGenerator
from states.main_menu import MainMenu
from utils.palette import *
from utils.states import State


class Game:
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

        if not os.path.exists("assets/data/hydro_data.json"):
            try:
                self.data = DataLoader.combine_lake_river_data(
                    "lakes.json", "rivers.json", "assets/data/hydro_data.json"
                )
                print("Combined data generated from lakes.json and rivers.json")
            except Exception as e:
                print(f"Error combining data: {e}")
                self.data = []
        else:
            try:
                self.data = DataLoader.load_json_data("assets/data/hydro_data.json")
                print(f"Loaded {len(self.data)} years of data")
            except Exception as e:
                print(f"Error loading data: {e}")
                self.data = []

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

            match self.state.state:
                case "MAIN_MENU":
                    self.main_menu.handle_events(event)
                case "WATER":
                    pass
                case "POLUTION":
                    pass
                case "TEMPERATURE":
                    pass
                case "GENERATE_REPORT":
                    self.generate_report()
                    self.state.change_state("MAIN_MENU")

    def generate_report(self):
        """
        Generate a PDF report from the loaded data
        """
        if not self.data:
            print("No data available to generate report")
            return

        try:
            timestamp = pygame.time.get_ticks()
            report_path = f"reports/hydro_report_{timestamp}.pdf"

            full_path = PDFReportGenerator.generate_report(self.data, report_path)
            print(f"Report generated: {full_path}")

            try:
                import platform
                import subprocess

                if platform.system() == "Darwin":
                    subprocess.call(("open", full_path))
                # elif platform.system() == "Windows":
                #     os.startfile(full_path)
                else:
                    subprocess.call(("xdg-open", full_path))
            except Exception as e:
                print(f"Could not open PDF automatically: {e}")

        except Exception as e:
            print(f"Error generating report: {e}")

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
                pass
            case "POLUTION":
                pass
            case "TEMPERATURE":
                pass

        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
