import pygame

from utils.button import Button
from utils.data_loader import DataLoader
from utils.report_generation import ReportGenerator
from utils.ui import UI


class Water:
    def __init__(self) -> None:
        self.generate_button = Button("assets/graphics/water_report.png", (800, 750))

        self.data_loader = DataLoader()
        self.report_generation = ReportGenerator()

        self.map1s = pygame.image.load("assets/maps/level/map_level_21.png")
        self.map1r = self.map1s.get_rect(center=(1000, 400))

        self.ui = UI()

    def handle_events(self, ev: pygame.event.Event):
        self.ui.handle_events(ev)

        if self.generate_button.is_clicked(ev):
            data = self.data_loader.load_json_data("hydro_data.json")

            if data and self.data_loader.validate_data(data):
                success = self.report_generation.generate_water_level_report(data)
                if success:
                    print("Raport poziomu wody został wygenerowany pomyślnie!")
                else:
                    print("Błąd podczas generowania raportu poziomu wody!")

    def render(self, w: pygame.surface.Surface):
        w.blit(self.map1s, self.map1r)

        self.generate_button.render(w)
        self.ui.render(w)
