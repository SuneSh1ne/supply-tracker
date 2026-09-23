"""Тесты для модуля storage."""
import os
from storage import load_deliveries, save_deliveries, DELIVERIES_FILE


def test_save_and_load_deliveries():
    test_data = [
        {
            "id": 1, "supplier_name": "Test Supplier", "product_name": "Test Product",
            "quantity": 5, "price": 10.0, "total_cost": 50.0, "delivery_date": "01.01.2026",
            "is_paid": True, "is_valid": True, "status": "Поставка принята на склад"
        }
    ]
    
    # Сохраняем тестовые данные
    save_deliveries(test_data, DELIVERIES_FILE)
    
    # Загружаем и проверяем
    loaded_data = load_deliveries(DELIVERIES_FILE)
    assert len(loaded_data) == 1
    assert loaded_data[0]["supplier_name"] == "Test Supplier"
    
    # Очистка после теста
    if os.path.exists(DELIVERIES_FILE):
        os.remove(DELIVERIES_FILE)