"""Модуль для работы с товарами."""
from typing import List, Optional


class Product:
    """Класс, описывающий товар."""

    def __init__(self, product_id: int, name: str, price: float) -> None:
        self.id = product_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.name} (Цена: {self.price:.2f} руб.)"

    @staticmethod
    def validate_price(price: float) -> bool:
        """Проверить корректность цены."""
        return price > 0

    @classmethod
    def from_data(cls, data: dict) -> "Product":
        """Создать объект из словаря."""
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"]
        )


def add_product(products: List[Product], name: str, price: float) -> Product:
    """Добавить новый товар."""
    new_id = max((p.id for p in products), default=0) + 1
    product = Product(new_id, name, price)
    products.append(product)
    return product


def find_product_by_id(products: List[Product], product_id: int) -> Optional[Product]:
    """Найти товар по ID."""
    return next((p for p in products if p.id == product_id), None)


def show_products(products: List[Product]) -> None:
    """Вывести список товаров."""
    if not products:
        print("Список товаров пуст.")
        return
    print(f"{'ID':<5} | {'Название':<30} | {'Цена':<10}")
    print("-" * 50)
    for p in products:
        print(f"{p.id:<5} | {p.name:<30} | {p.price:<10.2f}")