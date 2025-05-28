import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)


class ReportGenerator:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()

    def generate_water_level_report(self, data: dict, filename: str = ""):
        if not data:
            print("Błąd: Brak danych do wygenerowania raportu.")
            return

        if filename == "":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"raport_poziom_wod_{timestamp}.pdf"

        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []

        title = Paragraph(f"Raport Poziomu Wód", self.styles["Title"])
        story.append(title)
        story.append(Spacer(1, 0.2 * inch))

        date_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        story.append(Paragraph(f"Data generacji: {date_str}", self.styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

        lokalizacja = data.get("lokalizacja", "Brak danych o lokalizacji")
        story.append(
            Paragraph(f"Lokalizacja: <b>{lokalizacja}</b>", self.styles["Normal"])
        )
        story.append(Spacer(1, 0.2 * inch))

        water_measurements = data.get("pomiar_wody", [])
        if water_measurements:
            story.append(Paragraph("Szczegóły pomiarów:", self.styles["h2"]))
            story.append(Spacer(1, 0.1 * inch))

            table_data = [["Data", "Poziom", "Jednostka"]]
            for entry in water_measurements:
                table_data.append(
                    [
                        entry.get("data", "N/A"),
                        str(entry.get("poziom", "N/A")),
                        entry.get("jednostka", "N/A"),
                    ]
                )

            table = Table(table_data)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 0.2 * inch))
        else:
            story.append(
                Paragraph(
                    "Brak szczegółowych danych pomiarowych.", self.styles["Normal"]
                )
            )
            story.append(Spacer(1, 0.2 * inch))

        try:
            doc.build(story)
            print(f"Raport PDF '{filepath}' został pomyślnie wygenerowany.")
        except Exception as e:
            print(f"Błąd podczas generowania raportu PDF: {e}")
