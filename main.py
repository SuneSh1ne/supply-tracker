"""Начальный сценарий сервиса учёта поставок.

Реализует три функции, описанные в README.md:
    - validate_delivery — проверка корректности данных поставки;
    - calculate_total_cost — расчёт итоговой стоимости поставки;
    - get_delivery_status — определение статуса поставки.
"""

from datetime import date


def validate_delivery(
    supplier_name: str,
    product_name: str,
    quantity: int,
    price: float,
) -> bool:
    """Проверяет корректность данных поставки.

    Args:
        supplier_name: название поставщика.
        product_name: название товара.
        quantity: количество единиц товара.
        price: цена за единицу товара.

    Returns:
        True, если данные корректны, иначе False.
    """
    if not supplier_name or not product_name:
        return False
    if quantity <= 0:
        return False
    if price <= 0:
        return False
    return True


def calculate_total_cost(quantity: int, price: float) -> float:
    """Считает итоговую стоимость поставки.

    Args:
        quantity: количество единиц товара.
        price: цена за единицу товара.

    Returns:
        Итоговая стоимость поставки.
    """
    return quantity * price


def get_delivery_status(is_valid: bool, is_paid: bool) -> str:
    """Определяет статус поставки.

    Args:
        is_valid: прошла ли поставка валидацию.
        is_paid: оплачена ли поставка.

    Returns:
        Строка со статусом поставки.
    """
    if not is_valid:
        return "Поставка отклонена: некорректные данные"
    if not is_paid:
        return "Поставка ожидает оплаты"
    return "Поставка принята на склад"


def main() -> None:
    """Запускает демонстрационный сценарий учёта поставки."""
    supplier_name = "ООО Ромашка"
    product_name = "Кабель UTP cat.5e"
    quantity = 500
    price = 24.5
    is_paid = True
    delivery_date = date(2026, 9, 15)

    is_valid = validate_delivery(
        supplier_name, product_name, quantity, price
    )
    total_cost = calculate_total_cost(quantity, price)
    status = get_delivery_status(is_valid, is_paid)

    print(f"Поставщик: {supplier_name}")
    print(f"Товар: {product_name}")
    print(f"Количество: {quantity} шт.")
    print(f"Цена за единицу: {price:.2f} руб.")
    print(f"Дата поставки: {delivery_date}")
    print(f"Итоговая стоимость: {total_cost:.2f} руб.")
    print(f"Статус: {status}")


if __name__ == "__main__":
    main()