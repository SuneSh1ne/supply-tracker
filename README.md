# Supply Tracker — сервис учёта поставок

Консольное и веб-приложение для учёта поступлений товаров на склад от поставщиков.
Проект развивается поэтапно: консольная версия на Python дополнена веб-интерфейсом
на Django, а слой доступа к данных переведён с JSON и ручных SQL-запросов на Django ORM.

## 1. Назначение проекта

Supply Tracker — учебное приложение для складской логистики.

Приложение позволяет:
* просматривать поставки, поставщиков и товары в браузере;
* просматривать подробную информацию о конкретной поставке, поставщике и товаре;
* искать поставки по названию поставщика или товара;
* фильтровать поставки по дате, поставщику, товару и цене товара;
* сортировать список поставок по дате, поставщику, товару и количеству;
* просматривать поставки постранично;
* искать поставки и свободных поставщиков на выбранную дату;
* просматривать статистику количества и стоимости поставок по поставщикам;
* рассчитывать итоговую стоимость поставки;
* отслеживать статус поставки (принята / ожидает оплаты / отменена);
* добавлять поставки, поставщиков и товары, отменять поставки (консольная версия);
* хранить данные между запусками приложения.

## 2. Используемые технологии

* Python 3;
* Django 5.2 — веб-фреймворк;
* Django ORM — доступ к данным через модели;
* SQLite — СУБД (целевая база `db.sqlite3`, исходная база ПР7 `data/supplytracker.sqlite`);
* SQL — предыдущая реализация слоя данных (ПР7);
* Django Template Language (DTL);
* HTML5, CSS3, JavaScript;
* Bootstrap 5.3;
* JSON — исходное хранилище данных (ПР2–ПР6);
* Git;
* pytest;
* flake8.

## 3. Предметная область

Основные объекты предметной области:
* поставщик;
* товар;
* поставка.

Поставка связывает поставщика и товар: фиксирует факт поступления определённого
количества товара от конкретного поставщика на указанную дату.
Одна поставка относится к одному поставщику и одному товару;
один поставщик и один товар могут участвовать в нескольких поставках.
Отменённая поставка не удаляется из системы, а меняет статус — информация о ней сохраняется
и не учитывается в статистике и поиске свободных поставщиков.

## 4. Основные сущности

### Supplier — поставщик

Консольный класс (`models/suppliers.py`) и модель Django (`suppliers/models.py`).

Поля модели:
* `id` — первичный ключ (создаётся Django автоматически);
* `name` — название поставщика (`CharField`).

Обратная связь: `supplier.deliveries.all()` — поставки поставщика
(`related_name="deliveries"`).

### Product — товар

Консольный класс (`models/products.py`) и модель Django (`products/models.py`).

Поля модели:
* `id` — первичный ключ;
* `name` — название товара (`CharField`);
* `price` — цена за единицу (`DecimalField`).

Обратная связь: `product.deliveries.all()` — поставки товара.

### Delivery — поставка

Консольный класс (`models/deliveries.py`) и модель Django (`deliveries/models.py`).

Поля модели:
* `id` — первичный ключ;
* `supplier` — внешний ключ на `Supplier` (`on_delete=PROTECT`, `related_name="deliveries"`);
* `product` — внешний ключ на `Product` (`on_delete=PROTECT`, `related_name="deliveries"`);
* `quantity` — количество единиц товара (`PositiveIntegerField`);
* `delivery_date` — дата поставки (`DateField`);
* `is_paid` — признак оплаты (`BooleanField`, по умолчанию `False`);
* `is_cancelled` — признак отмены (`BooleanField`, по умолчанию `False`).

Методы модели:
* `calculate_total_cost()` — расчёт итоговой стоимости поставки;
* `cancel()` — отмена поставки с сохранением изменения в базе;
* `__str__()` — строковое представление поставки.

Параметр `on_delete=PROTECT` запрещает удаление поставщика или товара,
на которых ссылаются поставки: история поставок сохраняется.

## 5. Страницы веб-интерфейса

| Страница | URL | View-функция | Источник данных |
|----------|-----|--------------|-----------------|
| Главная | `/` | `homepage.views.index` | — |
| Список поставок | `/deliveries/` | `deliveries.views.deliveries_list` | ORM: фильтры, поиск, сортировка, пагинация |
| Поиск по дате | `/deliveries/available/` | `deliveries.views.available_deliveries` | ORM: `filter`, `exclude`, `values_list` |
| Статистика | `/deliveries/statistics/` | `deliveries.views.statistics` | ORM: `annotate`, `Count`, `Sum`, `Coalesce` |
| Поставка | `/deliveries/<int:delivery_id>/` | `deliveries.views.delivery_detail` | ORM: `get_object_or_404`, `select_related` |
| Список поставщиков | `/suppliers/` | `suppliers.views.suppliers_list` | ORM: `all()` |
| Поставщик | `/suppliers/<int:supplier_id>/` | `suppliers.views.supplier_detail` | ORM: `get_object_or_404` |
| Список товаров | `/products/` | `products.views.products_list` | ORM: `all()` |
| Товар | `/products/<int:product_id>/` | `products.views.product_detail` | ORM: `get_object_or_404` |

Если объект с указанным идентификатором не найден, возвращается код статуса 404
и собственная страница ошибки (`templates/404.html`). Внутренние ошибки сервера
отображаются через `templates/500.html`.

## 6. Слой данных

### 6.1 Django ORM (ПР9)

Структура базы данных описана моделями Django и управляется миграциями:
* миграции созданы командами `makemigrations suppliers products deliveries` и применены `migrate`;
* файлы миграций хранятся в приложениях и включены в репозиторий;
* целевая база данных — `db.sqlite3` (настройка `DATABASES` по умолчанию); в репозиторий не включается.

Используемые ORM-запросы (не менее 15 различных выражений):

| Категория | Примеры в проекте |
|-----------|-------------------|
| Получение наборов | `Delivery.objects.all()`, `Supplier.objects.all()`, `Product.objects.all()` |
| Получение одного объекта | `get_object_or_404(Delivery.objects.select_related(...), pk=...)` |
| Фильтрация по одному условию | `filter(delivery_date=selected_date)` |
| Фильтрация по нескольким условиям | цепочка `filter(...)` по дате, поставщику и товару |
| Фильтрация по связанной модели | `filter(product__price__gte=price)`, `filter(supplier_id=...)` |
| Исключение записей | `Supplier.objects.exclude(pk__in=busy_deliveries.values_list("supplier_id", flat=True))` |
| Поиск по строковому полю | `supplier__name__icontains=query` |
| Поиск по нескольким полям | `Q(supplier__name__icontains=q) \| Q(product__name__icontains=q)` |
| Сортировка | `order_by(sort_field, "id")`, в т.ч. по связанному полю `supplier__name` |
| Связи | `select_related("supplier", "product")`, обратная связь `supplier.deliveries` |
| Агрегирование | `Count("deliveries", filter=Q(...))`, `Sum(F(...) * F(...), filter=Q(...))`, `Coalesce`, `count()` |
| Аннотирование | `annotate(supplier_name=F("name"), deliveries_count=..., total_cost=...)` |
| Постраничный вывод | `Paginator`, `get_page()`, навигация через `{% querystring %}` |

Безопасность запросов:
* поле сортировки выбирается через словарь разрешённых соответствий `SORT_FIELDS`,
  произвольный пользовательский ввод в `order_by()` не передаётся;
* даты и числа, полученные из запроса, проверяются и преобразуются до использования;
* отсутствующие объекты обрабатываются через `get_object_or_404`, пустые результаты — через `{% empty %}`.

### 6.2 Перенос данных

История переноса данных по этапам проекта:
1. ПР2–ПР6: данные хранятся в JSON-файлах `data/suppliers.json`, `data/products.json`, `data/deliveries.json`;
2. ПР7: данные перенесены из JSON в SQLite-базу `data/supplytracker.sqlite` скриптом `db/import_json.py`;
3. ПР9: данные перенесены из `data/supplytracker.sqlite` в целевую базу Django `db.sqlite3`
   скриптом `db/import_sqlite_to_orm.py` (`update_or_create`, `transaction.atomic`,
   сохранение первичных ключей и связей; строки дат `ДД.ММ.ГГГГ` преобразуются в объекты `date`).

Исходная база ПР7 сохранена как источник данных; перед переносом создаётся резервная копия
`data/supplytracker_backup.sqlite`. Инспекция исходной базы выполняется скриптом
`db/inspect_source_db.py`.

### 6.3 SQL-слой ПР7 (сохранён как предыдущая реализация)

Файлы SQL-слоя остаются в проекте как предыдущая реализация предметной области;
представления после ПР9 их не используют:
* `sql/schema.sql` — скрипт создания таблиц `suppliers`, `products`, `deliveries` с первичными и внешними ключами;
* `sql/queries.sql` — SQL-запросы проекта (списки, `WHERE`, `JOIN`, агрегатные функции, `GROUP BY`, `HAVING`, параметризованные запросы);
* `db/database.py` — подключение к SQLite с `PRAGMA foreign_keys = ON`;
* `db/import_json.py` — однократный перенос данных из JSON в SQLite.

## 7. Шаблоны и статические файлы (ПР6)

* базовый шаблон `templates/base.html` с блоками `{% block title %}` и `{% block content %}`;
* навигация вынесена в `templates/includes/navigation.html` и подключается через `{% include %}`;
* дочерние шаблоны наследуют базовый через `{% extends "base.html" %}`;
* повторяющиеся фрагменты вынесены во включаемые шаблоны (например, `deliveries/includes/delivery_status.html`);
* данные передаются из представлений через контекст; в шаблонах используются циклы `{% for %}`,
  условия `{% if %}`, `{% empty %}`, фильтры (`length`, `default`, `date`, `floatformat`);
* ссылки формируются через именованные маршруты `{% url %}` с пространствами имён приложений;
* статические файлы приложения `homepage`: `css/style.css`, `js/main.js`, `img/logo.png`,
  подключаются через `{% load static %}` и `{% static %}`;
* JavaScript выводит текущий год в подвале страниц.

## 8. Структура проекта

```text
supply-tracker/
├── manage.py                  # точка входа Django
├── main.py                    # консольная версия приложения (ПР3)
├── storage.py                 # загрузка и сохранение JSON (ПР3)
├── utils.py                   # функции безопасного ввода (ПР3)
├── conftest.py                # конфигурация pytest
├── requirements.txt
├── README.md
├── .flake8
├── .gitignore
├── supplytracker/             # пакет настроек Django-проекта
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/                 # шаблоны уровня проекта
│   ├── base.html
│   ├── 404.html
│   ├── 500.html
│   └── includes/
│       └── navigation.html
├── homepage/                  # приложение: главная страница и статика
│   ├── migrations/
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── templates/homepage/
│   │   └── index.html
│   ├── urls.py
│   └── views.py
├── deliveries/                # приложение: поставки
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── templates/deliveries/
│   │   ├── delivery_list.html
│   │   ├── delivery_detail.html
│   │   ├── available.html
│   │   ├── statistics.html
│   │   └── includes/
│   │       └── delivery_status.html
│   ├── models.py              # модель Delivery
│   ├── urls.py
│   └── views.py
├── suppliers/                 # приложение: поставщики
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── templates/suppliers/
│   │   ├── supplier_list.html
│   │   └── supplier_detail.html
│   ├── models.py              # модель Supplier
│   ├── urls.py
│   └── views.py
├── products/                  # приложение: товары
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── templates/products/
│   │   ├── product_list.html
│   │   └── product_detail.html
│   ├── models.py              # модель Product
│   ├── urls.py
│   └── views.py
├── models/                    # классы предметной области (ПР3)
│   ├── __init__.py
│   ├── suppliers.py
│   ├── products.py
│   └── deliveries.py
├── db/                        # слой работы с базами данных
│   ├── __init__.py
│   ├── database.py            # подключение к SQLite (ПР7)
│   ├── import_json.py         # перенос JSON → SQLite (ПР7)
│   ├── inspect_source_db.py   # инспекция исходной базы (ПР9)
│   └── import_sqlite_to_orm.py# перенос SQLite → Django ORM (ПР9)
├── sql/                       # SQL-скрипты (ПР7)
│   ├── schema.sql
│   └── queries.sql
├── data/                      # данные приложения
│   ├── suppliers.json
│   ├── products.json
│   ├── deliveries.json
│   ├── supplytracker.sqlite       # исходная база ПР7 (не в репозитории)
│   └── supplytracker_backup.sqlite# резервная копия (не в репозитории)
├── tests/                     # автоматизированные тесты pytest
│   ├── __init__.py
│   ├── test_suppliers.py
│   ├── test_products.py
│   └── test_deliveries.py
└── db.sqlite3                 # целевая база Django (не в репозитории)
## 9. Назначение основных модулей

* `main.py` — консольная версия приложения: меню, сценарии работы с объектами;
* `models/` — классы предметной области ПР3 (`Supplier`, `Product`, `Delivery`) и функции работы с коллекциями;
* `storage.py` — преобразование JSON ↔ объекты Python;
* `utils.py` — безопасный консольный ввод чисел, дат и ответов «да/нет»;
* `supplytracker/` — настройки проекта, корневая маршрутизация, точки входа серверов;
* `homepage/`, `deliveries/`, `suppliers/`, `products/` — Django-приложения: модели, представления, маршруты и шаблоны соответствующих сущностей;
* `db/` — скрипты подключения, инспекции и переноса данных между хранилищами;
* `sql/` — схема базы и SQL-запросы предыдущей реализации (ПР7);
* `tests/` — тесты классов предметной области.