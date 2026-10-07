"""View-функции для товаров."""
from django.http import HttpResponse

from homepage.views import page
from models.products import find_product_by_id
from storage import load_products


def products_list(request):
    """Список товаров."""
    products = load_products()

    items = ""
    for p in products:
        items += f"""
        <li class="list-group-item d-flex
            justify-content-between align-items-center">
            <a href="/products/{p.id}/">{p.name}</a>
            <span class="badge bg-info">
                {p.price:.2f} руб.
            </span>
        </li>
        """

    content = f"""
    <h1>Товары</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Товары", content))


def product_detail(request, product_id):
    """Страница товара."""
    products = load_products()
    product = find_product_by_id(products, product_id)

    if product is None:
        content = """
        <h1 class="text-danger">Товар не найден</h1>
        <a href="/products/" class="btn btn-outline-secondary">
            ← К списку товаров
        </a>
        """
        return HttpResponse(
            page("Товар не найден", content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{product.name}</h5>
            <p class="card-text">
                <strong>ID:</strong> {product.id}
            </p>
            <p class="card-text">
                <strong>Цена:</strong>
                {product.price:.2f} руб.
            </p>
            <a href="/products/"
               class="btn btn-outline-secondary">
                ← К списку товаров
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(product.name, content),
        status=200,
    )
