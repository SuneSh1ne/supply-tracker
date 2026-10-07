from models.products import Product


def test_product_creation():
    p = Product(1, "Кабель", 25.5)
    assert p.id == 1
    assert p.price == 25.5


def test_product_validate_price():
    assert Product.validate_price(10.0) is True
    assert Product.validate_price(0) is False
