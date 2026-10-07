"""Модуль для работы с поставщиками."""
from typing import List, Optional


class Supplier:
    """Класс, описывающий поставщика."""

    def __init__(self, supplier_id: int, name: str) -> None:
        self.id = supplier_id
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.id})"

    @classmethod
    def from_data(cls, data: dict) -> "Supplier":
        """Создать объект из словаря (при загрузке из JSON)."""
        return cls(supplier_id=data["id"], name=data["name"])


def add_supplier(suppliers: List[Supplier], name: str) -> Supplier:
    """Добавить нового поставщика."""
    new_id = max((s.id for s in suppliers), default=0) + 1
    supplier = Supplier(new_id, name)
    suppliers.append(supplier)
    return supplier


def find_supplier_by_id(suppliers: List[Supplier], supplier_id: int) -> Optional[Supplier]:
    """Найти поставщика по ID."""
    return next((s for s in suppliers if s.id == supplier_id), None)


def show_suppliers(suppliers: List[Supplier]) -> None:
    """Вывести список поставщиков."""
    if not suppliers:
        print("Список поставщиков пуст.")
        return
    print(f"{'ID':<5} | {'Название':<30}")
    print("-" * 40)
    for s in suppliers:
        print(f"{s.id:<5} | {s.name:<30}")
