"""View-функции для поставщиков (SQLite)."""
import sqlite3

from django.shortcuts import render

from db.database import get_connection
from models.suppliers import find_supplier_by_id
from storage import load_suppliers


def suppliers_list(request):
    """Список поставщиков из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    suppliers_data = conn.execute(
        "SELECT id, name FROM suppliers ORDER BY id;"
    ).fetchall()
    conn.close()
    return render(
        request,
        "suppliers/supplier_list.html",
        {"suppliers": suppliers_data},
    )


def supplier_detail(request, supplier_id):
    """Страница поставщика."""
    suppliers = load_suppliers()
    supplier = find_supplier_by_id(suppliers, supplier_id)
    return render(
        request,
        "suppliers/supplier_detail.html",
        {"supplier": supplier},
        status=404 if supplier is None else 200,
    )
