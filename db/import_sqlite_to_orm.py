"""Перенос данных из базы ПР7 в модели Django ORM."""
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "supplytracker.sqlite"

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supplytracker.settings")
django.setup()

from deliveries.models import Delivery  # noqa: E402
from products.models import Product  # noqa: E402
from suppliers.models import Supplier  # noqa: E402

DATE_FORMAT = "%d.%m.%Y"


def main():
    """Перенести данные из исходной базы в модели Django."""
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        suppliers = connection.execute(
            "SELECT id, name FROM suppliers ORDER BY id"
        ).fetchall()
        products = connection.execute(
            "SELECT id, name, price FROM products ORDER BY id"
        ).fetchall()
        deliveries = connection.execute(
            """
            SELECT id, supplier_id, product_id, quantity,
                   delivery_date, is_paid, is_cancelled
            FROM deliveries ORDER BY id
            """
        ).fetchall()

    with transaction.atomic():
        for row in suppliers:
            Supplier.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"]},
            )
        for row in products:
            Product.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"], "price": row["price"]},
            )
        for row in deliveries:
            delivery_date = datetime.strptime(
                row["delivery_date"], DATE_FORMAT
            ).date()
            Delivery.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "supplier_id": row["supplier_id"],
                    "product_id": row["product_id"],
                    "quantity": row["quantity"],
                    "delivery_date": delivery_date,
                    "is_paid": bool(row["is_paid"]),
                    "is_cancelled": bool(row["is_cancelled"]),
                },
            )

    print("Перенос данных завершён.")
    print("Поставщиков:", Supplier.objects.count())
    print("Товаров:", Product.objects.count())
    print("Поставок:", Delivery.objects.count())


if __name__ == "__main__":
    main()
