"""View-функции для поставок (с использованием SQLite)."""
import sqlite3
from datetime import datetime

from django.shortcuts import render

from db.database import get_connection
from models.deliveries import find_delivery_by_id
from storage import load_deliveries, load_products, load_suppliers

DATE_FORMAT = "%d.%m.%Y"


def is_valid_date(date_str: str) -> bool:
    """Проверить, что строка является датой в формате ДД.ММ.ГГГГ."""
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False


def deliveries_list(request):
    """Список всех поставок из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    deliveries_data = conn.execute("""
        SELECT
            deliveries.id,
            deliveries.delivery_date,
            deliveries.quantity,
            deliveries.is_paid,
            deliveries.is_cancelled,
            suppliers.name AS supplier_name,
            products.name AS product_name,
            products.price AS product_price
        FROM deliveries
        JOIN suppliers ON deliveries.supplier_id = suppliers.id
        JOIN products ON deliveries.product_id = products.id
        ORDER BY deliveries.id;
    """).fetchall()
    conn.close()
    return render(
        request,
        "deliveries/delivery_list.html",
        {"deliveries": deliveries_data},
    )


def delivery_detail(request, delivery_id):
    """Страница конкретной поставки (из JSON через ПР3)."""
    suppliers = load_suppliers()
    products = load_products()
    deliveries = load_deliveries(suppliers, products)
    delivery = find_delivery_by_id(deliveries, delivery_id)
    context = {"delivery": delivery}
    return render(
        request,
        "deliveries/delivery_detail.html",
        context,
        status=404 if delivery is None else 200,
    )


def available_deliveries(request):
    """Поиск по дате: поставки на дату и свободные поставщики."""
    delivery_date = request.GET.get("date", "").strip()
    error = ""
    deliveries_on_date = []
    free_suppliers = []

    if delivery_date:
        if not is_valid_date(delivery_date):
            error = (
                "Некорректная дата: введите в формате ДД.ММ.ГГГГ, "
                "например 15.09.2026."
            )
        else:
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            deliveries_on_date = conn.execute(
                """
                SELECT
                    deliveries.id,
                    deliveries.delivery_date,
                    deliveries.quantity,
                    suppliers.name AS supplier_name,
                    products.name AS product_name
                FROM deliveries
                JOIN suppliers
                    ON deliveries.supplier_id = suppliers.id
                JOIN products
                    ON deliveries.product_id = products.id
                WHERE deliveries.delivery_date = ?
                  AND deliveries.is_cancelled = 0
                ORDER BY deliveries.id;
                """,
                [delivery_date],
            ).fetchall()
            free_suppliers = conn.execute(
                """
                SELECT suppliers.id, suppliers.name
                FROM suppliers
                WHERE suppliers.id NOT IN (
                    SELECT deliveries.supplier_id
                    FROM deliveries
                    WHERE deliveries.delivery_date = ?
                      AND deliveries.is_cancelled = 0
                )
                ORDER BY suppliers.id;
                """,
                [delivery_date],
            ).fetchall()
            conn.close()

    context = {
        "delivery_date": delivery_date,
        "error": error,
        "deliveries_on_date": deliveries_on_date,
        "free_suppliers": free_suppliers,
    }
    return render(request, "deliveries/available.html", context)


def statistics(request):
    """Страница статистики: количество и стоимость по поставщикам."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    stats = conn.execute("""
        SELECT
            suppliers.name AS supplier_name,
            COUNT(deliveries.id) AS deliveries_count,
            COALESCE(SUM(deliveries.quantity * products.price), 0) AS total_cost
        FROM suppliers
        LEFT JOIN deliveries
            ON suppliers.id = deliveries.supplier_id
            AND deliveries.is_cancelled = 0
        LEFT JOIN products
            ON deliveries.product_id = products.id
        GROUP BY suppliers.id, suppliers.name
        ORDER BY total_cost DESC;
    """).fetchall()
    conn.close()
    return render(
        request,
        "deliveries/statistics.html",
        {"statistics": stats},
    )
