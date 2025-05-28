import pygame

from utils.button import Button
from utils.data_loader import DataLoader
from utils.report_generation import ReportGenerator
from utils.ui import UI


class Polution:
    def __init__(self) -> None:
        self.generate_button = Button("assets/graphics/polution_report.png", (800, 750))

        self.data_loader = DataLoader()
        self.report_generation = ReportGenerator()

        self.ui = UI()

    def handle_events(self, ev: pygame.event.Event):
        self.ui.handle_events(ev)

        if self.generate_button.is_clicked(ev):
            data = self.data_loader.load_json_data("hydro_data.json")

            if data:
                self.report_generation.generate_water_level_report(data)

    def render(self, w: pygame.surface.Surface):
        self.generate_button.render(w)
        self.ui.render(w)
