"""View-функции для товаров."""
from django.shortcuts import render

from models.products import find_product_by_id
from storage import load_products


def products_list(request):
    """Список товаров."""
    products = load_products()

    context = {
        "products": products,
    }
    return render(request, "products/product_list.html", context)


def product_detail(request, product_id):
    """Страница товара."""
    products = load_products()
    product = find_product_by_id(products, product_id)

    context = {
        "product": product,
    }
    return render(
        request,
        "products/product_detail.html",
        context,
        status=404 if product is None else 200,
    )
