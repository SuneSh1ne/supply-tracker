"""View-функции для товаров (SQLite)."""
import sqlite3

from django.shortcuts import render

from db.database import get_connection
from models.products import find_product_by_id
from storage import load_products


def products_list(request):
    """Список товаров из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    products_data = conn.execute(
        "SELECT id, name, price FROM products ORDER BY id;"
    ).fetchall()
    conn.close()
    return render(
        request,
        "products/product_list.html",
        {"products": products_data},
    )


def product_detail(request, product_id):
    """Страница товара."""
    products = load_products()
    product = find_product_by_id(products, product_id)
    return render(
        request,
        "products/product_detail.html",
        {"product": product},
        status=404 if product is None else 200,
    )
