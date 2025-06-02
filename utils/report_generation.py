import os
from datetime import datetime
from typing import Any, Dict

import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)


class ReportGenerator:
    def __init__(self, reports_dir: str = "reports", assets_dir: str = "assets"):
        self.reports_dir = reports_dir
        self.assets_dir = assets_dir
        self.font_path = os.path.join(assets_dir, "fonts")

        os.makedirs(reports_dir, exist_ok=True)
        os.makedirs(self.font_path, exist_ok=True)

        self._register_fonts()

    def _register_fonts(self):
        """Rejestruje czcionki dla PDF"""
        try:
            font_files = {
                "Helvetica": "Helvetica.ttf",
                "Helvetica-Bold": "Helvetica.ttf",
            }

            for font_name, filename in font_files.items():
                font_file = os.path.join(self.font_path, filename)
                if os.path.exists(font_file):
                    pdfmetrics.registerFont(TTFont(font_name, font_file))
                    print(f"Zarejestrowano czcionkę: {font_name}")
                else:
                    print(
                        f"Uwaga: Nie znaleziono czcionki {filename} w {self.font_path}"
                    )
                    print("Używam czcionek systemowych")

        except Exception as e:
            print(f"Błąd podczas rejestracji czcionek: {e}")
            print("Używam czcionek domyślnych")

    def _create_styles(self):
        styles = getSampleStyleSheet()

        try:
            title_font = (
                "DejaVuSans-Bold"
                if "DejaVuSans-Bold" in pdfmetrics.getRegisteredFontNames()
                else "Helvetica-Bold"
            )
            body_font = (
                "DejaVuSans"
                if "DejaVuSans" in pdfmetrics.getRegisteredFontNames()
                else "Helvetica"
            )
        except:
            title_font = "Helvetica-Bold"
            body_font = "Helvetica"

        custom_styles = {
            "CustomTitle": ParagraphStyle(
                "CustomTitle",
                parent=styles["Title"],
                fontName=title_font,
                fontSize=20,
                spaceAfter=30,
                alignment=1,  # Wyśrodkowanie
            ),
            "CustomHeading": ParagraphStyle(
                "CustomHeading",
                parent=styles["Heading1"],
                fontName=title_font,
                fontSize=14,
                spaceAfter=12,
                textColor=colors.darkblue,
            ),
            "CustomBody": ParagraphStyle(
                "CustomBody",
                parent=styles["Normal"],
                fontName=body_font,
                fontSize=11,
                spaceAfter=12,
            ),
        }

        return custom_styles

    def _analyze_trends(self, data: Dict[str, Any]) -> Dict[str, str]:
        years = []
        avg_levels = []
        temperatures = []

        for year_data in data["data_pomiarow"]:
            years.append(year_data["year"])
            avg_levels.append(year_data["average_water_level"])
            temperatures.append(year_data["temperature"])

        trends = {}

        if len(avg_levels) >= 2:
            water_trend = np.polyfit(years, avg_levels, 1)[0]
            if water_trend > 1:
                trends["water"] = (
                    "Poziom wody wykazuje trend wzrostowy. Prognoza na przyszłość: stabilny lub rosnący poziom wód."
                )
            elif water_trend < -1:
                trends["water"] = (
                    "Poziom wody wykazuje trend spadkowy. Prognoza na przyszłość: możliwe dalsze obniżanie się poziomu wód."
                )
            else:
                trends["water"] = (
                    "Poziom wody pozostaje relatywnie stabilny. Prognoza na przyszłość: utrzymanie obecnych poziomów."
                )

        if len(temperatures) >= 2:
            temp_trend = np.polyfit(years, temperatures, 1)[0]
            if temp_trend > 0.2:
                trends["temperature"] = (
                    "Temperatura wykazuje trend wzrostowy. Może to wpływać na ekosystem wodny."
                )
            elif temp_trend < -0.2:
                trends["temperature"] = "Temperatura wykazuje trend spadkowy."
            else:
                trends["temperature"] = "Temperatura pozostaje stabilna."

        return trends

    def _create_chart(
        self, data: Dict[str, Any], chart_type: str = "water_level"
    ) -> str:
        """Tworzy wykres i zwraca ścieżkę do pliku"""
        plt.style.use("default")
        fig, ax = plt.subplots(figsize=(10, 6))

        years = [year_data["year"] for year_data in data["data_pomiarow"]]

        filename = "chart.png"

        if chart_type == "water_level":
            values = [
                year_data["average_water_level"] for year_data in data["data_pomiarow"]
            ]
            ax.plot(
                years, values, marker="o", linewidth=2, markersize=8, color="#2E86AB"
            )
            ax.set_ylabel("Średni poziom wody (cm)", fontsize=12)
            ax.set_title(
                "Średni poziom wody w jeziorach mazurskich",
                fontsize=14,
                fontweight="bold",
            )
            filename = "water_level_chart.png"

        elif chart_type == "temperature":
            values = [year_data["temperature"] for year_data in data["data_pomiarow"]]
            ax.plot(
                years, values, marker="s", linewidth=2, markersize=8, color="#A23B72"
            )
            ax.set_ylabel("Temperatura (°C)", fontsize=12)
            ax.set_title(
                "Średnia temperatura w rejonie jezior mazurskich",
                fontsize=14,
                fontweight="bold",
            )
            filename = "temperature_chart.png"

        ax.set_xlabel("Rok", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(years)

        plt.tight_layout()

        chart_path = os.path.join(self.reports_dir, filename)
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()

        return chart_path

    def generate_water_level_report(self, data: Dict[str, Any]) -> bool:
        try:
            pdf_path = os.path.join(self.reports_dir, "raport_poziom_wody.pdf")

            doc = SimpleDocTemplate(pdf_path, pagesize=A4)
            story = []

            styles = self._create_styles()

            title = Paragraph(
                f"Raport: {data['nazwa_projektu']}", styles["CustomTitle"]
            )
            story.append(title)
            story.append(Spacer(1, 20))

            info_text = f"""
            <b>Lokalizacja:</b> {data['lokalizacja']}<br/>
            <b>Okres badań:</b> {data['data_pomiarow'][0]['year']} - {data['data_pomiarow'][-1]['year']}<br/>
            <b>Data generacji raportu:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
            """
            info = Paragraph(info_text, styles["CustomBody"])
            story.append(info)
            story.append(Spacer(1, 20))

            chart_path = self._create_chart(data, "water_level")
            if os.path.exists(chart_path):
                img = Image(chart_path, width=6 * inch, height=3.6 * inch)
                story.append(img)
                story.append(Spacer(1, 20))

            story.append(
                Paragraph("Szczegółowe dane pomiarowe", styles["CustomHeading"])
            )

            table_data = [["Rok", "Średni poziom wody (cm)", "Temperatura (°C)"]]
            for year_data in data["data_pomiarow"]:
                table_data.append(
                    [
                        str(year_data["year"]),
                        f"{year_data['average_water_level']:.2f}",
                        f"{year_data['temperature']:.1f}",
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
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            story.append(table)
            story.append(Spacer(1, 20))

            trends = self._analyze_trends(data)
            story.append(
                Paragraph("Analiza trendów i prognoza", styles["CustomHeading"])
            )

            if "water" in trends:
                trend_para = Paragraph(trends["water"], styles["CustomBody"])
                story.append(trend_para)

            if "temperature" in trends:
                temp_para = Paragraph(trends["temperature"], styles["CustomBody"])
                story.append(temp_para)

            story.append(Spacer(1, 20))
            story.append(Paragraph("Podsumowanie", styles["CustomHeading"]))

            summary_text = f"""
            Na podstawie analizy danych z lat {data['data_pomiarow'][0]['year']}-{data['data_pomiarow'][-1]['year']} 
            można stwierdzić, że stan wód w regionie jezior mazurskich wymaga dalszego monitorowania. 
            Regularne pomiary pozwolą na lepsze zrozumienie zmian zachodzących w ekosystemie wodnym 
            i podjęcie odpowiednich działań ochronnych w przyszłości.
            """
            summary = Paragraph(summary_text, styles["CustomBody"])
            story.append(summary)

            doc.build(story)

            print(f"Raport został wygenerowany: {pdf_path}")
            return True

        except Exception as e:
            print(f"Błąd podczas generowania raportu: {e}")
            return False

    def generate_temperature_report(self, data: Dict[str, Any]) -> bool:
        """Generuje raport PDF o temperaturze"""
        try:
            pdf_path = os.path.join(self.reports_dir, "raport_temperatura.pdf")
            doc = SimpleDocTemplate(pdf_path, pagesize=A4)
            story = []
            styles = self._create_styles()

            title = Paragraph(
                f"Raport temperatury: {data['nazwa_projektu']}", styles["CustomTitle"]
            )
            story.append(title)
            story.append(Spacer(1, 20))

            chart_path = self._create_chart(data, "temperature")
            if os.path.exists(chart_path):
                img = Image(chart_path, width=6 * inch, height=3.6 * inch)
                story.append(img)
                story.append(Spacer(1, 20))

            trends = self._analyze_trends(data)
            if "temperature" in trends:
                analysis = Paragraph(
                    f"Analiza: {trends['temperature']}", styles["CustomBody"]
                )
                story.append(analysis)

            doc.build(story)
            print(f"Raport temperatury został wygenerowany: {pdf_path}")
            return True

        except Exception as e:
            print(f"Błąd podczas generowania raportu temperatury: {e}")
            return False

    def generate_pollution_report(self, data: Dict[str, Any]) -> bool:
        try:
            pdf_path = os.path.join(self.reports_dir, "raport_zanieczyszczenia.pdf")
            doc = SimpleDocTemplate(pdf_path, pagesize=A4)
            story = []
            styles = self._create_styles()

            title = Paragraph(
                f"Raport zanieczyszczeń: {data['nazwa_projektu']}",
                styles["CustomTitle"],
            )
            story.append(title)
            story.append(Spacer(1, 20))

            info = Paragraph(
                "Dane o zanieczyszczeniach będą dostępne po rozszerzeniu struktury danych.",
                styles["CustomBody"],
            )
            story.append(info)

            doc.build(story)
            print(f"Raport zanieczyszczeń został wygenerowany: {pdf_path}")
            return True

        except Exception as e:
            print(f"Błąd podczas generowania raportu zanieczyszczeń: {e}")
            return False
