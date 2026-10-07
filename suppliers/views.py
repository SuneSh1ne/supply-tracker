"""View-функции для поставщиков."""
from django.http import HttpResponse

from homepage.views import page
from models.suppliers import find_supplier_by_id
from storage import load_suppliers


def suppliers_list(request):
    """Список поставщиков."""
    suppliers = load_suppliers()

    items = ""
    for s in suppliers:
        items += f"""
        <li class="list-group-item">
            <a href="/suppliers/{s.id}/">{s.name}</a>
        </li>
        """

    content = f"""
    <h1>Поставщики</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Поставщики", content))


def supplier_detail(request, supplier_id):
    """Страница поставщика."""
    suppliers = load_suppliers()
    supplier = find_supplier_by_id(suppliers, supplier_id)

    if supplier is None:
        content = """
        <h1 class="text-danger">Поставщик не найден</h1>
        <a href="/suppliers/" class="btn btn-outline-secondary">
            ← К списку поставщиков
        </a>
        """
        return HttpResponse(
            page("Поставщик не найден", content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{supplier.name}</h5>
            <p class="card-text">
                <strong>ID:</strong> {supplier.id}
            </p>
            <a href="/suppliers/"
               class="btn btn-outline-secondary">
                ← К списку поставщиков
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(supplier.name, content),
        status=200,
    )
