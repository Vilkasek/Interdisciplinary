import json
import os


class DataLoader:
    def __init__(self, base_path="assets/data"):
        self.base_path = base_path

    def _get_full_path(self, filename: str) -> str:
        return os.path.join(self.base_path, filename)

    def load_json_data(self, filename: str):
        filepath = self._get_full_path(filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            print(f"Błąd: Plik '{filepath}' nie został znaleziony.")
            return None
        except json.JSONDecodeError:
            print(
                f"Błąd: Nie można zdekodować pliku '{filepath}'. Upewnij się, że jest to prawidłowy plik JSON."
            )
            return None
        except Exception as e:
            print(
                f"Wystąpił nieoczekiwany błąd podczas ładowania pliku '{filepath}': {e}"
            )
            return None
