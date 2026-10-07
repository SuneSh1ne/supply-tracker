from models.suppliers import Supplier
from models.products import Product
from models.deliveries import Delivery, add_delivery


def test_delivery_creation():
    s = Supplier(1, "Поставщик")
    p = Product(1, "Товар", 10.0)
    d = Delivery(1, s, p, 5, "01.01.2026", is_paid=True)
    assert d.calculate_total_cost() == 50.0
    assert d.get_status() == "Поставка принята на склад"


def test_delivery_cancel():
    s = Supplier(1, "Поставщик")
    p = Product(1, "Товар", 10.0)
    d = Delivery(1, s, p, 5, "01.01.2026")
    d.cancel()
    assert d.is_cancelled is True
    assert d.get_status() == "Поставка отменена"


def test_add_delivery():
    deliveries = []
    s = Supplier(1, "Поставщик")
    p = Product(1, "Товар", 10.0)
    d = add_delivery(deliveries, s, p, 5, "01.01.2026", False)
    assert len(deliveries) == 1
    assert d.get_status() == "Поставка ожидает оплаты"
