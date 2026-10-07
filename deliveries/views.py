"""View-функции для поставок."""
from django.http import HttpResponse

from homepage.views import page
from models.deliveries import find_delivery_by_id
from storage import (
    load_deliveries,
    load_products,
    load_suppliers,
)


def deliveries_list(request):
    """Список всех поставок."""
    suppliers = load_suppliers()
    products = load_products()
    deliveries = load_deliveries(suppliers, products)

    items = ""
    for d in deliveries:
        badge = "bg-secondary" if d.is_cancelled else "bg-success"
        status = "Отменена" if d.is_cancelled else d.get_status()
        items += f"""
        <li class="list-group-item d-flex justify-content-between
            align-items-center">
            <a href="/deliveries/{d.id}/">
                Поставка #{d.id}: {d.product.name}
                от {d.supplier.name}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """

    content = f"""
    <h1>Поставки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Поставки", content))


def delivery_detail(request, delivery_id):
    """Страница конкретной поставки."""
    suppliers = load_suppliers()
    products = load_products()
    deliveries = load_deliveries(suppliers, products)

    delivery = find_delivery_by_id(deliveries, delivery_id)
    if delivery is None:
        content = """
        <h1 class="text-danger">Поставка не найдена</h1>
        <a href="/deliveries/" class="btn btn-outline-secondary">
            ← К списку поставок
        </a>
        """
        return HttpResponse(
            page("Поставка не найдена", content),
            status=404,
        )

    badge = "bg-secondary" if delivery.is_cancelled else "bg-success"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                Поставка #{delivery.id}
            </h5>
            <p class="card-text">
                <strong>Поставщик:</strong>
                {delivery.supplier.name}
            </p>
            <p class="card-text">
                <strong>Товар:</strong>
                {delivery.product.name}
            </p>
            <p class="card-text">
                <strong>Количество:</strong>
                {delivery.quantity} шт.
            </p>
            <p class="card-text">
                <strong>Цена за единицу:</strong>
                {delivery.product.price:.2f} руб.
            </p>
            <p class="card-text">
                <strong>Итоговая стоимость:</strong>
                {delivery.calculate_total_cost():.2f} руб.
            </p>
            <p class="card-text">
                <strong>Дата поставки:</strong>
                {delivery.delivery_date}
            </p>
            <p class="card-text">
                <strong>Оплачено:</strong>
                {'Да' if delivery.is_paid else 'Нет'}
            </p>
            <p class="card-text">
                <strong>Статус:</strong>
                <span class="badge {badge}">
                    {delivery.get_status()}
                </span>
            </p>
            <a href="/deliveries/"
               class="btn btn-outline-secondary">
                ← К списку поставок
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Поставка #{delivery.id}", content),
        status=200,
    )
