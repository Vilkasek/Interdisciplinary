import pygame

from utils.button import Button
from utils.data_loader import DataLoader
from utils.report_generation import ReportGenerator
from utils.ui import UI


class Temperature:
    def __init__(self) -> None:
        self.generate_button = Button(
            "assets/graphics/temperature_report.png", (800, 750)
        )

        self.data_loader = DataLoader()
        self.report_generation = ReportGenerator()

        self.map1s = pygame.image.load("assets/maps/temperature/map_temp_21.png")
        self.map1r = self.map1s.get_rect(center=(1000, 400))

        self.ui = UI()

    def handle_events(self, ev: pygame.event.Event):
        self.ui.handle_events(ev)

        if self.generate_button.is_clicked(ev):
            data = self.data_loader.load_json_data("hydro_data.json")

            if data and self.data_loader.validate_data(data):
                success = self.report_generation.generate_temperature_report(data)
                if success:
                    print("Raport temperatury został wygenerowany pomyślnie!")
                else:
                    print("Błąd podczas generowania raportu temperatury!")

    def render(self, w: pygame.surface.Surface):
        w.blit(self.map1s, self.map1r)

        self.generate_button.render(w)
        self.ui.render(w)
