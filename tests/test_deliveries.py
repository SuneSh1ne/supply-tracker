"""Тесты для модуля deliveries."""
from deliveries import add_delivery, find_delivery, validate_delivery, calculate_total_cost


def test_validate_delivery_valid():
    assert validate_delivery("ООО Ромашка", "Кабель", 10, 5.5) is True


def test_validate_delivery_invalid_quantity():
    assert validate_delivery("ООО Ромашка", "Кабель", 0, 5.5) is False


def test_calculate_total_cost():
    assert calculate_total_cost(10, 5.5) == 55.0


def test_add_delivery():
    deliveries = []
    add_delivery(deliveries, 1, "ООО Ромашка", "Кабель", 10, 5.5, "15.09.2026", True)
    assert len(deliveries) == 1
    assert deliveries[0]["supplier_name"] == "ООО Ромашка"
    assert deliveries[0]["total_cost"] == 55.0
    assert deliveries[0]["status"] == "Поставка принята на склад"


def test_find_delivery():
    deliveries = []
    add_delivery(deliveries, 1, "ООО Ромашка", "Кабель UTP", 10, 5.5, "15.09.2026", True)
    add_delivery(deliveries, 2, "ЗАО Лилия", "Провод", 5, 10.0, "16.09.2026", False)
    
    found = find_delivery(deliveries, "кабель")
    assert len(found) == 1
    assert found[0]["id"] == 1