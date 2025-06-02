import json
import os
from typing import Any, Dict, Optional


class DataLoader:
    def __init__(self, data_dir: str = "assets/data"):
        self.data_dir = data_dir

    def load_json_data(self, filename: str) -> Optional[Dict[str, Any]]:
        filepath = os.path.join(self.data_dir, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                print(f"Pomyślnie załadowano dane z: {filepath}")
                return data
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {filepath}")
            return None
        except json.JSONDecodeError as e:
            print(f"Błąd parsowania JSON: {e}")
            return None
        except Exception as e:
            print(f"Nieoczekiwany błąd podczas ładowania danych: {e}")
            return None

    def validate_data(self, data: Dict[str, Any]) -> bool:
        required_keys = ["nazwa_projektu", "lokalizacja", "data_pomiarow"]

        if not all(key in data for key in required_keys):
            print("Błąd: Brakuje wymaganych kluczy w danych")
            return False

        if not isinstance(data["data_pomiarow"], list):
            print("Błąd: 'data_pomiarow' musi być listą")
            return False

        for year_data in data["data_pomiarow"]:
            if not all(
                key in year_data
                for key in [
                    "year",
                    "water_bodies",
                    "average_water_level",
                    "temperature",
                ]
            ):
                print(
                    f"Błąd: Niepoprawna struktura danych dla roku {year_data.get('year', 'nieznany')}"
                )
                return False

        return True
