"""View-функции для поставщиков (Django ORM)."""
from django.shortcuts import get_object_or_404, render

from suppliers.models import Supplier


def suppliers_list(request):
    """Список поставщиков."""
    suppliers_data = Supplier.objects.all()
    return render(
        request,
        "suppliers/supplier_list.html",
        {"suppliers": suppliers_data},
    )


def supplier_detail(request, supplier_id):
    """Страница поставщика."""
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    return render(
        request,
        "suppliers/supplier_detail.html",
        {"supplier": supplier},
    )
