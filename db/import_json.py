"""Перенос данных из JSON-файлов в базу SQLite."""
import json

from db.database import get_connection

SUPPLIERS_FILE = "data/suppliers.json"
PRODUCTS_FILE = "data/products.json"
DELIVERIES_FILE = "data/deliveries.json"


def load_json(filename):
    """Загрузить JSON-файл."""
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def import_suppliers(conn):
    """Импортировать поставщиков."""
    suppliers = load_json(SUPPLIERS_FILE)
    conn.executemany(
        "INSERT INTO suppliers (id, name) VALUES (?, ?)",
        [(s["id"], s["name"]) for s in suppliers],
    )


def import_products(conn):
    """Импортировать товары."""
    products = load_json(PRODUCTS_FILE)
    conn.executemany(
        "INSERT INTO products (id, name, price) VALUES (?, ?, ?)",
        [(p["id"], p["name"], p["price"]) for p in products],
    )


def import_deliveries(conn):
    """Импортировать поставки."""
    deliveries = load_json(DELIVERIES_FILE)
    conn.executemany(
        """
        INSERT INTO deliveries
        (id, supplier_id, product_id, quantity, delivery_date, is_paid, is_cancelled)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                d["id"],
                d["supplier_id"],
                d["product_id"],
                d["quantity"],
                d["delivery_date"],
                int(d["is_paid"]),
                int(d["is_cancelled"]),
            )
            for d in deliveries
        ],
    )


def main():
    """Точка запуска импорта."""
    conn = get_connection()
    try:
        import_suppliers(conn)
        import_products(conn)
        import_deliveries(conn)
        conn.commit()
        print("Данные успешно импортированы в SQLite.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка импорта: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
