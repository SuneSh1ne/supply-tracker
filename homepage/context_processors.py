"""Общие данные для шаблонов Supply Tracker."""
from deliveries.models import Delivery
from products.models import Product
from suppliers.models import Supplier


def site_context(request):
    """Передаёт название сайта и счётчики сущностей в шаблоны."""
    return {
        "site_name": "Supply Tracker",
        "suppliers_count": Supplier.objects.count(),
        "products_count": Product.objects.count(),
        "deliveries_count": Delivery.objects.count(),
    }
