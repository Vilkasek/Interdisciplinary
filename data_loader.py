import json
import os
from typing import Dict, List


class DataLoader:
    @staticmethod
    def load_json_data(filepath: str) -> List[Dict]:
        """
        Load data from a JSON file.

        :param filepath: Path to the JSON file
        :return: List of dictionaries containing the data
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {filepath}")
        except Exception as e:
            raise RuntimeError(f"Error reading file {filepath}: {str(e)}")

    @staticmethod
    def combine_lake_river_data(
        lakes_file: str,
        rivers_file: str,
        output_file: str = "assets/data/hydro_data.json",
    ) -> List[Dict]:
        """
        Combine lake and river data into a single structured JSON file.

        :param lakes_file: Path to lakes JSON file
        :param rivers_file: Path to rivers JSON file
        :param output_file: Path to save the combined data
        :return: Combined data as a list of dictionaries
        """
        try:
            lakes_data = DataLoader.load_json_data(lakes_file)
            rivers_data = DataLoader.load_json_data(rivers_file)

            years = []
            if lakes_data and len(lakes_data) > 0:
                first_lake_row = lakes_data[0]
                for key, value in first_lake_row.items():
                    if isinstance(value, int) and value >= 2000:
                        years.append(value)

                for col_name in ["Column3", "Column4"]:
                    if col_name in first_lake_row and isinstance(
                        first_lake_row[col_name], int
                    ):
                        years.append(first_lake_row[col_name])

            years = sorted(set(years))

            combined_data = []

            for year in years:
                year_data = {
                    "year": year,
                    "water_bodies": {"lakes": [], "rivers": []},
                    "average_water_level": 0,
                    "temperature": 15.0 + (year - 2020) * 0.8,
                }

                for lake_entry in lakes_data[1:]:
                    lake_name = lake_entry.get("Nazwa zbiornika ", "")
                    lake_level = None

                    if year == lakes_data[0].get(
                        "Średnia wysokość zwierciadła [m]  ", None
                    ):
                        lake_level = lake_entry.get(
                            "Średnia wysokość zwierciadła [m]  ", None
                        )
                    elif year == lakes_data[0].get("Column3", None):
                        lake_level = lake_entry.get("Column3", None)
                    elif year == lakes_data[0].get("Column4", None):
                        lake_level = lake_entry.get("Column4", None)

                    if lake_level and lake_level != "Brak danych":
                        try:
                            lake_level = float(lake_level)
                        except (ValueError, TypeError):
                            lake_level = None
                    else:
                        lake_level = None

                    year_data["water_bodies"]["lakes"].append(
                        {"name": lake_name, "water_level": lake_level}
                    )

                for river_entry in rivers_data[1:]:
                    river_name = river_entry.get("Nazwa cieku ", "")
                    river_level = None

                    if year == rivers_data[0].get(
                        "Średnia wysokość lustra wody [m]", None
                    ):
                        river_level = river_entry.get(
                            "Średnia wysokość lustra wody [m]", None
                        )
                    elif year == rivers_data[0].get("Column3", None):
                        river_level = river_entry.get("Column3", None)
                    elif year == rivers_data[0].get("Column4", None):
                        river_level = river_entry.get("Column4", None)

                    if river_level and river_level != "Brak danych":
                        try:
                            river_level = float(river_level)
                        except (ValueError, TypeError):
                            river_level = None
                    else:
                        river_level = None

                    year_data["water_bodies"]["rivers"].append(
                        {"name": river_name, "water_level": river_level}
                    )

                valid_levels = []

                for lake in year_data["water_bodies"]["lakes"]:
                    if lake["water_level"] is not None:
                        valid_levels.append(lake["water_level"])

                for river in year_data["water_bodies"]["rivers"]:
                    if river["water_level"] is not None:
                        valid_levels.append(river["water_level"])

                if valid_levels:
                    year_data["average_water_level"] = sum(valid_levels) / len(
                        valid_levels
                    )

                combined_data.append(year_data)

            if output_file:
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(combined_data, f, indent=2, ensure_ascii=False)

            return combined_data

        except Exception as e:
            raise RuntimeError(f"Error combining data: {str(e)}")
