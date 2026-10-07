"""Модуль для сохранения и загрузки данных."""
import json
import os
from typing import List, Dict, Any

from models.suppliers import Supplier
from models.products import Product
from models.deliveries import Delivery

DATA_DIR = "data"
SUPPLIERS_FILE = os.path.join(DATA_DIR, "suppliers.json")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
DELIVERIES_FILE = os.path.join(DATA_DIR, "deliveries.json")


def ensure_data_dir() -> None:
    """Создать директорию для данных."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_json(filename: str) -> List[Dict[str, Any]]:
    """Загрузить данные из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка при чтении {filename}: {e}")
        return []


def save_json(filename: str, data: List[Dict[str, Any]]) -> None:
    """Сохранить данные в JSON-файл."""
    ensure_data_dir()
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка при записи {filename}: {e}")


def load_suppliers() -> List[Supplier]:
    """Загрузить список поставщиков."""
    data = load_json(SUPPLIERS_FILE)
    return [Supplier.from_data(d) for d in data]


def save_suppliers(suppliers: List[Supplier]) -> None:
    """Сохранить список поставщиков."""
    data = [{"id": s.id, "name": s.name} for s in suppliers]
    save_json(SUPPLIERS_FILE, data)


def load_products() -> List[Product]:
    """Загрузить список товаров."""
    data = load_json(PRODUCTS_FILE)
    return [Product.from_data(d) for d in data]


def save_products(products: List[Product]) -> None:
    """Сохранить список товаров."""
    data = [{"id": p.id, "name": p.name, "price": p.price} for p in products]
    save_json(PRODUCTS_FILE, data)


def load_deliveries(suppliers: List[Supplier], products: List[Product]) -> List[Delivery]:
    """Загрузить список поставок с восстановлением связей."""
    data = load_json(DELIVERIES_FILE)
    deliveries = []
    for d in data:
        try:
            deliveries.append(Delivery.from_data(d, suppliers, products))
        except ValueError as e:
            print(f"Пропуск некорректной записи: {e}")
    return deliveries


def save_deliveries(deliveries: List[Delivery]) -> None:
    """Сохранить список поставок."""
    data = [
        {
            "id": d.id,
            "supplier_id": d.supplier.id,
            "product_id": d.product.id,
            "quantity": d.quantity,
            "delivery_date": d.delivery_date,
            "is_paid": d.is_paid,
            "is_cancelled": d.is_cancelled
        } for d in deliveries
    ]
    save_json(DELIVERIES_FILE, data)
