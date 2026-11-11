"""View-функции для товаров (Django ORM)."""
from django.shortcuts import get_object_or_404, render

from products.models import Product


def products_list(request):
    """Список товаров."""
    products_data = Product.objects.all()
    return render(
        request,
        "products/product_list.html",
        {"products": products_data},
    )


def product_detail(request, product_id):
    """Страница товара."""
    product = get_object_or_404(Product, pk=product_id)
    return render(
        request,
        "products/product_detail.html",
        {"product": product},
    )
