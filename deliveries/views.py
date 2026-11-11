"""View-функции для поставок (Django ORM)."""
from datetime import datetime
from decimal import Decimal

from django.core.paginator import Paginator
from django.db.models import Count, DecimalField, F, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, render

from deliveries.models import Delivery
from products.models import Product
from suppliers.models import Supplier

DATE_FORMAT = "%d.%m.%Y"
PAGE_SIZE = 5

SORT_FIELDS = {
    "date": "delivery_date",
    "supplier": "supplier__name",
    "product": "product__name",
    "quantity": "quantity",
}


def deliveries_list(request):
    """Список поставок: фильтры, поиск, сортировка, пагинация."""
    delivery_date = request.GET.get("date", "").strip()
    supplier_id = request.GET.get("supplier", "").strip()
    product_id = request.GET.get("product", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "date")
    error = None

    deliveries_data = Delivery.objects.select_related("supplier", "product")

    if delivery_date:
        try:
            selected_date = datetime.strptime(delivery_date, DATE_FORMAT).date()
        except ValueError:
            error = "Некорректная дата: введите в формате ДД.ММ.ГГГГ."
        else:
            deliveries_data = deliveries_data.filter(delivery_date=selected_date)

    if supplier_id.isdigit():
        deliveries_data = deliveries_data.filter(supplier_id=int(supplier_id))
    if product_id.isdigit():
        deliveries_data = deliveries_data.filter(product_id=int(product_id))

    if min_price:
        try:
            price = float(min_price.replace(",", "."))
        except ValueError:
            error = error or "Некорректная цена: введите число."
        else:
            deliveries_data = deliveries_data.filter(product__price__gte=price)

    if query:
        deliveries_data = deliveries_data.filter(
            Q(supplier__name__icontains=query) | Q(product__name__icontains=query)
        )

    sort_field = SORT_FIELDS.get(sort, "delivery_date")
    deliveries_data = deliveries_data.order_by(sort_field, "id")

    paginator = Paginator(deliveries_data, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "deliveries": page_obj,
        "page_obj": page_obj,
        "delivery_date": delivery_date,
        "selected_supplier": supplier_id,
        "selected_product": product_id,
        "min_price": min_price,
        "query": query,
        "sort": sort,
        "suppliers": Supplier.objects.order_by("name"),
        "products": Product.objects.order_by("name"),
        "error": error,
    }
    return render(request, "deliveries/delivery_list.html", context)


def delivery_detail(request, delivery_id):
    """Страница конкретной поставки."""
    delivery = get_object_or_404(
        Delivery.objects.select_related("supplier", "product"),
        pk=delivery_id,
    )
    return render(
        request,
        "deliveries/delivery_detail.html",
        {"delivery": delivery},
    )


def available_deliveries(request):
    """Поиск по дате: поставки на дату и свободные поставщики."""
    delivery_date = request.GET.get("date", "").strip()
    error = None
    deliveries_on_date = []
    free_suppliers = []

    if delivery_date:
        try:
            selected_date = datetime.strptime(delivery_date, DATE_FORMAT).date()
        except ValueError:
            error = "Некорректная дата: введите в формате ДД.ММ.ГГГГ."
        else:
            busy_deliveries = Delivery.objects.filter(
                delivery_date=selected_date,
                is_cancelled=False,
            )
            deliveries_on_date = busy_deliveries.select_related(
                "supplier", "product"
            ).order_by("id")
            free_suppliers = Supplier.objects.exclude(
                pk__in=busy_deliveries.values_list("supplier_id", flat=True)
            ).order_by("id")

    context = {
        "delivery_date": delivery_date,
        "error": error,
        "deliveries_on_date": deliveries_on_date,
        "free_suppliers": free_suppliers,
    }
    return render(request, "deliveries/available.html", context)


def statistics(request):
    """Статистика: количество и стоимость поставок по поставщикам."""
    statistics_data = Supplier.objects.annotate(
        supplier_name=F("name"),
        deliveries_count=Count(
            "deliveries",
            filter=Q(deliveries__is_cancelled=False),
        ),
        total_cost=Coalesce(
            Sum(
                F("deliveries__quantity") * F("deliveries__product__price"),
                filter=Q(deliveries__is_cancelled=False),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            ),
            Value(
                Decimal("0.00"),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            ),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        ),
    ).order_by("-total_cost")
    return render(
        request,
        "deliveries/statistics.html",
        {"statistics": statistics_data},
    )
