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
                return json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {filepath}")
        except Exception as e:
            raise RuntimeError(f"Error reading file {filepath}: {str(e)}")
