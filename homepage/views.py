"""Главная страница приложения."""
from django.http import HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Единый каркас всех страниц проекта."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Supply Tracker</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/deliveries/">Поставки</a>
                <a class="nav-link" href="/suppliers/">Поставщики</a>
                <a class="nav-link" href="/products/">Товары</a>
            </div>
        </div>
    </nav>
    <main class="container">
        {content}
    </main>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">Supply Tracker</h1>
    <p class="lead">Сервис учёта поставок товаров на склад.</p>
    <p>Приложение позволяет отслеживать поставки от поставщиков,
    контролировать количество и стоимость товаров.</p>
    <a href="/deliveries/" class="btn btn-primary me-2">Поставки</a>
    <a href="/suppliers/" class="btn btn-secondary me-2">Поставщики</a>
    <a href="/products/" class="btn btn-outline-secondary">Товары</a>
    """
    return HttpResponse(page("Supply Tracker", content))
