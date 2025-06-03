import pygame

from utils.button import Button
from utils.data_loader import DataLoader
from utils.report_generation import ReportGenerator
from utils.ui import UI
from utils.states import State

class Water:
    def __init__(self) -> None:
        self.generate_button = Button("assets/graphics/water_report.png", (800, 750))

        self.data_loader = DataLoader()
        self.report_generation = ReportGenerator()

        self.map1sl = pygame.image.load("assets/maps/level/map_level_21.png")
        self.map1rl = self.map1sl.get_rect(center=(1000, 400))

        self.map1sr = pygame.image.load("assets/maps/temperature/Poz21.png")
        self.map1rr = self.map1sr.get_rect(center=(1000, 400))

        self.state = State()
        
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
        self.image = self.state.image

        match self.image:
            case 1:
                w.blit(self.map1sl, self.map1rl)
            case 2:
                w.blit(self.map1sr, self.map1rr)

        self.generate_button.render(w)
        self.ui.render(w)
