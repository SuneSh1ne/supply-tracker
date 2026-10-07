"""Модуль для работы с поставками."""
from typing import List, Optional

from models.suppliers import Supplier
from models.products import Product


class Delivery:
    """Класс, описывающий поставку."""

    def __init__(
        self,
        delivery_id: int,
        supplier: Supplier,
        product: Product,
        quantity: int,
        delivery_date: str,
        is_paid: bool = False,
        is_cancelled: bool = False
    ) -> None:
        self.id = delivery_id
        self.supplier = supplier
        self.product = product
        self.quantity = quantity
        self.delivery_date = delivery_date
        self.is_paid = is_paid
        self.is_cancelled = is_cancelled

    def calculate_total_cost(self) -> float:
        """Рассчитать итоговую стоимость."""
        return self.quantity * self.product.price

    def get_status(self) -> str:
        """Определить статус поставки."""
        if self.is_cancelled:
            return "Поставка отменена"
        if self.quantity <= 0:
            return "Поставка отклонена: некорректное количество"
        if not self.is_paid:
            return "Поставка ожидает оплаты"
        return "Поставка принята на склад"

    def cancel(self) -> None:
        """Отменить поставку."""
        self.is_cancelled = True

    def __str__(self) -> str:
        """Строковое представление поставки."""
        return (
            f"Поставка #{self.id}: {self.product.name} от {self.supplier.name}, "
            f"Кол-во: {self.quantity}, Стоимость: {self.calculate_total_cost():.2f} руб., "
            f"Дата: {self.delivery_date}, Статус: {self.get_status()}"
        )

    @classmethod
    def from_data(cls, data: dict, suppliers: List[Supplier], products: List[Product]) -> "Delivery":
        """Восстановить объект поставки из JSON, связав с объектами поставщика и товара."""
        supplier = next((s for s in suppliers if s.id == data["supplier_id"]), None)
        product = next((p for p in products if p.id == data["product_id"]), None)
        if not supplier or not product:
            raise ValueError("Поставщик или товар не найдены")
        return cls(
            delivery_id=data["id"],
            supplier=supplier,
            product=product,
            quantity=data["quantity"],
            delivery_date=data["delivery_date"],
            is_paid=data.get("is_paid", False),
            is_cancelled=data.get("is_cancelled", False)
        )


def add_delivery(
    deliveries: List[Delivery],
    supplier: Supplier,
    product: Product,
    quantity: int,
    delivery_date: str,
    is_paid: bool
) -> Optional[Delivery]:
    """Создать и добавить новую поставку."""
    if quantity <= 0:
        print("Ошибка: количество должно быть больше 0.")
        return None
    new_id = max((d.id for d in deliveries), default=0) + 1
    delivery = Delivery(new_id, supplier, product, quantity, delivery_date, is_paid)
    deliveries.append(delivery)
    return delivery


def find_delivery(deliveries: List[Delivery], query: str) -> List[Delivery]:
    """Найти поставки по подстроке в имени поставщика или товара."""
    return [
        d for d in deliveries
        if query.lower() in d.supplier.name.lower() or query.lower() in d.product.name.lower()
    ]


def find_delivery_by_id(
    deliveries: List[Delivery],
    delivery_id: int,
) -> Optional[Delivery]:
    """Найти поставку по идентификатору."""
    for delivery in deliveries:
        if delivery.id == delivery_id:
            return delivery
    return None


def filter_deliveries_by_status(deliveries: List[Delivery], status: str) -> List[Delivery]:
    """Отфильтровать поставки по статусу."""
    return [d for d in deliveries if d.get_status() == status]


def sort_deliveries_by_date(deliveries: List[Delivery]) -> List[Delivery]:
    """Отсортировать поставки по дате."""
    return sorted(deliveries, key=lambda x: x.delivery_date)


def show_deliveries(deliveries: List[Delivery]) -> None:
    """Вывести список поставок."""
    if not deliveries:
        print("Список поставок пуст.")
        return
    for d in deliveries:
        print(d)
