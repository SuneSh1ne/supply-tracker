"""Модуль для управления данными о поставках."""
from typing import List, Dict, Any


def validate_delivery(supplier_name: str, product_name: str, quantity: int, price: float) -> bool:
    """Проверяет корректность данных поставки."""
    if not supplier_name or not product_name:
        return False
    if quantity <= 0:
        return False
    if price <= 0:
        return False
    return True


def calculate_total_cost(quantity: int, price: float) -> float:
    """Считает итоговую стоимость поставки."""
    return quantity * price


def get_delivery_status(is_valid: bool, is_paid: bool) -> str:
    """Определяет статус поставки."""
    if not is_valid:
        return "Поставка отклонена: некорректные данные"
    if not is_paid:
        return "Поставка ожидает оплаты"
    return "Поставка принята на склад"


def add_delivery(
    deliveries: List[Dict[str, Any]],
    delivery_id: int,
    supplier_name: str,
    product_name: str,
    quantity: int,
    price: float,
    delivery_date: str,
    is_paid: bool
) -> None:
    """Добавить новую поставку в список."""
    is_valid = validate_delivery(supplier_name, product_name, quantity, price)
    total_cost = calculate_total_cost(quantity, price)
    status = get_delivery_status(is_valid, is_paid)
    
    delivery = {
        "id": delivery_id,
        "supplier_name": supplier_name,
        "product_name": product_name,
        "quantity": quantity,
        "price": price,
        "total_cost": total_cost,
        "delivery_date": delivery_date,
        "is_paid": is_paid,
        "is_valid": is_valid,
        "status": status
    }
    deliveries.append(delivery)


def find_delivery(deliveries: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """Найти поставки по подстроке в названии поставщика или товара (с использованием генератора)."""
    generator = (
        d for d in deliveries 
        if query.lower() in d["supplier_name"].lower() or query.lower() in d["product_name"].lower()
    )
    return list(generator)


def filter_deliveries_by_status(deliveries: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Отфильтровать поставки по статусу."""
    return [d for d in deliveries if d["status"] == status]


def sort_deliveries_by_date(deliveries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Отсортировать поставки по дате (с использованием lambda-функции)."""
    return sorted(deliveries, key=lambda x: x["delivery_date"])