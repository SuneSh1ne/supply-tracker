"""View-функции для поставщиков."""
from django.shortcuts import render

from models.suppliers import find_supplier_by_id
from storage import load_suppliers


def suppliers_list(request):
    """Список поставщиков."""
    suppliers = load_suppliers()

    context = {
        "suppliers": suppliers,
    }
    return render(request, "suppliers/supplier_list.html", context)


def supplier_detail(request, supplier_id):
    """Страница поставщика."""
    suppliers = load_suppliers()
    supplier = find_supplier_by_id(suppliers, supplier_id)

    context = {
        "supplier": supplier,
    }
    return render(
        request,
        "suppliers/supplier_detail.html",
        context,
        status=404 if supplier is None else 200,
    )
