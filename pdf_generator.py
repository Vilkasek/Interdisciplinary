import os
from datetime import datetime
from typing import Dict, List

import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle


class PDFReportGenerator:
    @staticmethod
    def generate_report(data: List[Dict], output_path=None):
        """
        Generate a PDF report with two tables:
        1. Historical data table
        2. Estimated data for the next year

        :param data: List of dictionaries containing historical data
        :param output_path: Path to save the PDF report
        """
        if output_path is None:
            output_path = f"hydro_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        doc = SimpleDocTemplate(output_path, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        heading_style = styles["Heading2"]

        elements.append(Paragraph("Hydro Mazury Report", title_style))
        elements.append(Paragraph("Historical and Projected Data", heading_style))

        table_data = [["Year", "Temperature (°C)", "Water Level (m)"]]
        for entry in data:
            table_data.append(
                [
                    str(entry.get("year", "N/A")),
                    str(entry.get("temperature", "N/A")),
                    str(entry.get("water_level", "N/A")),
                ]
            )

        historical_table = Table(table_data)
        historical_table.setStyle(
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
        elements.append(Paragraph("Historical Data", heading_style))
        elements.append(historical_table)

        if len(data) > 1:
            years = [entry["year"] for entry in data]
            temperatures = [entry["temperature"] for entry in data]
            water_levels = [entry["water_level"] for entry in data]

            temp_coeffs = np.polyfit(years, temperatures, 1)
            temp_model = np.poly1d(temp_coeffs)
            next_year = max(years) + 1
            estimated_temp = temp_model(next_year)

            water_coeffs = np.polyfit(years, water_levels, 1)
            water_model = np.poly1d(water_coeffs)
            estimated_water_level = water_model(next_year)

            projection_data = [
                ["Year", "Estimated Temperature (°C)", "Estimated Water Level (m)"],
                [
                    str(next_year),
                    f"{estimated_temp:.2f}",
                    f"{estimated_water_level:.2f}",
                ],
            ]

            projection_table = Table(projection_data)
            projection_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.lightblue),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            elements.append(Paragraph("Projected Data for Next Year", heading_style))
            elements.append(projection_table)

        doc.build(elements)

        return output_path
