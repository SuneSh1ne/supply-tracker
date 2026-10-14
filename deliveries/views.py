"""View-функции для поставок."""
from django.shortcuts import render

from models.deliveries import find_delivery_by_id
from storage import load_deliveries, load_products, load_suppliers


def deliveries_list(request):
    """Список всех поставок."""
    suppliers = load_suppliers()
    products = load_products()
    deliveries = load_deliveries(suppliers, products)

    context = {
        "deliveries": deliveries,
    }
    return render(request, "deliveries/delivery_list.html", context)


def delivery_detail(request, delivery_id):
    """Страница конкретной поставки."""
    suppliers = load_suppliers()
    products = load_products()
    deliveries = load_deliveries(suppliers, products)

    delivery = find_delivery_by_id(deliveries, delivery_id)

    context = {
        "delivery": delivery,
    }
    return render(
        request,
        "deliveries/delivery_detail.html",
        context,
        status=404 if delivery is None else 200,
    )
