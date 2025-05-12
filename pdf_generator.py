import os
import tempfile
from datetime import datetime
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Image, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)


class PDFReportGenerator:
    @staticmethod
    def generate_report(data: List[Dict], output_path=None):
        """
        Generate a PDF report with water data analysis

        :param data: List of dictionaries containing hydrological data
        :param output_path: Path to save the PDF report
        """
        if output_path is None:
            output_path = f"hydro_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        os.makedirs(
            os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
            exist_ok=True,
        )

        doc = SimpleDocTemplate(output_path, pagesize=landscape(letter))
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        heading_style = styles["Heading2"]
        normal_style = styles["Normal"]

        subtitle_style = ParagraphStyle(
            "Subtitle", parent=styles["Heading2"], fontSize=14, spaceAfter=12
        )

        elements.append(Paragraph("Hydro Mazury - Raport Hydrologiczny", title_style))
        elements.append(
            Paragraph(
                f"Wygenerowano: {datetime.now().strftime('%d.%m.%Y, %H:%M')}",
                subtitle_style,
            )
        )
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("1. Przegląd danych historycznych", heading_style))

        table_data = [["Rok", "Średni poziom wód [m]", "Temperatura [°C]"]]
        years = []
        avg_levels = []
        temperatures = []

        for entry in data:
            years.append(entry["year"])
            avg_levels.append(entry["average_water_level"])
            temperatures.append(entry["temperature"])

            table_data.append(
                [
                    str(entry["year"]),
                    f"{entry['average_water_level']:.2f}",
                    f"{entry['temperature']:.1f}",
                ]
            )

        historical_table = Table(table_data, colWidths=[1.5 * inch, 2 * inch, 2 * inch])
        historical_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.blue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.lightblue),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        elements.append(historical_table)
        elements.append(Spacer(1, 0.3 * inch))

        chart_path = PDFReportGenerator._create_trend_chart(
            years, avg_levels, temperatures
        )
        if chart_path:
            elements.append(
                Paragraph("Trend zmian poziomu wód i temperatury", subtitle_style)
            )
            img = Image(chart_path, width=7 * inch, height=3 * inch)
            elements.append(img)
            elements.append(Spacer(1, 0.3 * inch))

        elements.append(
            Paragraph("2. Szczegółowe dane zbiorników wodnych", heading_style)
        )

        for year_data in data:
            year = year_data["year"]
            elements.append(Paragraph(f"Rok {year}", subtitle_style))

            lake_data = [["Jezioro", "Poziom lustra wody [m]"]]
            for lake in year_data["water_bodies"]["lakes"]:
                if lake["water_level"] is not None:
                    lake_data.append([lake["name"], f"{lake['water_level']:.1f}"])
                else:
                    lake_data.append([lake["name"], "Brak danych"])

            lake_table = Table(lake_data, colWidths=[2 * inch, 2 * inch])
            lake_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.blue),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("ALIGN", (1, 0), (1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.lightblue),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            river_data = [["Rzeka", "Poziom lustra wody [m]"]]
            for river in year_data["water_bodies"]["rivers"]:
                river_data.append([river["name"], f"{river['water_level']:.1f}"])

            river_table = Table(river_data, colWidths=[2 * inch, 2 * inch])
            river_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.green),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("ALIGN", (1, 0), (1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.lightgreen),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            tables = [[lake_table, river_table]]
            combined_table = Table(tables, colWidths=[4.5 * inch, 4.5 * inch])
            combined_table.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("RIGHTPADDING", (0, 0), (0, 0), 10),
                    ]
                )
            )

            elements.append(combined_table)
            elements.append(Spacer(1, 0.3 * inch))

        if len(data) >= 2:
            elements.append(Paragraph("3. Prognoza na rok następny", heading_style))

            next_year = max(years) + 1

            water_coeffs = np.polyfit(years, avg_levels, 1)
            water_model = np.poly1d(water_coeffs)
            estimated_water_level = water_model(next_year)

            temp_coeffs = np.polyfit(years, temperatures, 1)
            temp_model = np.poly1d(temp_coeffs)
            estimated_temp = temp_model(next_year)

            forecast_data = [
                [
                    "Rok",
                    "Prognozowany średni poziom wód [m]",
                    "Prognozowana temperatura [°C]",
                ],
                [
                    str(next_year),
                    f"{estimated_water_level:.2f}",
                    f"{estimated_temp:.1f}",
                ],
            ]

            forecast_table = Table(forecast_data)
            forecast_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.orange),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.lightyellow),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            elements.append(forecast_table)

            water_trend = "wzrostowy" if water_coeffs[0] > 0 else "spadkowy"
            temp_trend = "wzrostowy" if temp_coeffs[0] > 0 else "spadkowy"

            elements.append(Spacer(1, 0.2 * inch))
            elements.append(
                Paragraph(
                    f"Analiza trendów historycznych wykazuje {water_trend} trend poziomu wód "
                    + f"({water_coeffs[0]:.2f} m/rok) oraz {temp_trend} trend temperatur "
                    + f"({temp_coeffs[0]:.2f}°C/rok).",
                    normal_style,
                )
            )

        doc.build(elements)

        if chart_path and os.path.exists(chart_path):
            os.remove(chart_path)

        return output_path

    @staticmethod
    def _create_trend_chart(years, water_levels, temperatures):
        """Create a chart showing water levels and temperature trends"""
        try:
            plt.figure(figsize=(10, 5))

            fig, ax1 = plt.subplots(figsize=(10, 5))
            ax2 = ax1.twinx()

            ax1.plot(years, water_levels, "b-o", label="Poziom wód")
            ax1.set_xlabel("Rok")
            ax1.set_ylabel("Poziom wód [m]", color="b")
            ax1.tick_params(axis="y", labelcolor="b")

            ax2.plot(years, temperatures, "r-^", label="Temperatura")
            ax2.set_ylabel("Temperatura [°C]", color="r")
            ax2.tick_params(axis="y", labelcolor="r")

            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

            plt.title("Zmiany poziomu wód i temperatury w czasie")
            plt.grid(True)
            plt.tight_layout()

            fd, temp_path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            plt.savefig(temp_path)
            plt.close()

            return temp_path
        except Exception as e:
            print(f"Error creating chart: {e}")
            return None
