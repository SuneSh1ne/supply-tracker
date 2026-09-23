"""Модуль для сохранения и загрузки данных в формате JSON."""
import json
import os
from typing import List, Dict, Any

DATA_DIR = "data"
DELIVERIES_FILE = os.path.join(DATA_DIR, "deliveries.json")


def ensure_data_dir() -> None:
    """Создает директорию для данных, если она не существует."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_deliveries(filename: str = DELIVERIES_FILE) -> List[Dict[str, Any]]:
    """Загрузить поставки из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        return []


def save_deliveries(deliveries: List[Dict[str, Any]], filename: str = DELIVERIES_FILE) -> None:
    """Сохранить поставки в JSON-файл."""
    ensure_data_dir()
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(deliveries, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка при записи в файл {filename}: {e}")