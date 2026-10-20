# Supply Tracker — сервис учёта поставок

## Назначение

Supply Tracker – приложение для управления поставками товаров на склад.
Консольная версия приложения (ПР3) дополнена веб-интерфейсом на Django (ПР5)
и переведена на систему шаблонов Django (ПР6).

Приложение позволяет:
* просматривать поставки в браузере;
* просматривать информацию о конкретной поставке;
* просматривать список поставщиков и товаров;
* просматривать информацию о поставщике и товаре;
* отслеживать статус поставки (принята / ожидает оплаты / отменена);
* рассчитывать итоговую стоимость поставки;
* добавлять поставки, поставщиков и товары (консольная версия);
* отменять поставки (консольная версия);
* искать поставки по названию поставщика или товара (консольная версия);
* хранить данные между запусками приложения.

## Используемые технологии

* Python 3;
* Django 5.2 – веб-фреймворк;
* Django Template Language (DTL);
* HTML5;
* CSS3;
* JavaScript;
* Bootstrap 5.3;
* JSON для хранения данных;
* Git;
* pytest;
* flake8.

## Целевая аудитория

* Кладовщики и сотрудники склада;
* Менеджеры по закупкам;
* Администраторы, ведущие справочники поставщиков и товаров.

## Предметная область

Основными объектами предметной области являются:
* поставщик;
* товар;
* поставка.

Поставка связывает поставщика и товар: фиксирует факт поступления определённого
количества товара от конкретного поставщика на указанную дату.
Одна поставка относится к одному поставщику и одному товару.
Отменённая поставка не удаляется из системы, а меняет статус — информация о ней сохраняется.

## Основные сущности

### Supplier – поставщик

Объект `Supplier` представляет организацию, поставляющую товары.

Основные атрибуты:
* `id` – уникальный идентификатор поставщика;
* `name` – название поставщика.

Основные методы:
* `__str__()` – строковое представление поставщика;
* `from_data()` – создание объекта `Supplier` из набора данных.

### Product – товар

Объект `Product` представляет товар с фиксированной ценой за единицу.

Основные атрибуты:
* `id` – уникальный идентификатор товара;
* `name` – название товара;
* `price` – цена за единицу товара.

Основные методы:
* `validate_price()` – статическая проверка корректности цены;
* `__str__()` – строковое представление товара;
* `from_data()` – создание объекта `Product` из набора данных.

### Delivery – поставка

Объект `Delivery` представляет факт поступления товара от поставщика.

Основные атрибуты:
* `id` – уникальный идентификатор поставки;
* `supplier` – объект `Supplier`;
* `product` – объект `Product`;
* `quantity` – количество единиц товара;
* `delivery_date` – дата поставки;
* `is_paid` – признак оплаты поставки;
* `is_cancelled` – признак отмены поставки.

Основные методы:
* `calculate_total_cost()` – расчёт итоговой стоимости поставки;
* `get_status()` – определение статуса поставки;
* `cancel()` – отмена поставки;
* `__str__()` – строковое представление поставки;
* `from_data()` – создание объекта `Delivery` из набора данных.

## Страницы веб-интерфейса

* `/` – главная страница: описание приложения и навигация (view-функция `index()`);
* `/deliveries/` – список поставок: объекты `Delivery` из `data/deliveries.json` (view-функция `deliveries_list()`);
* `/deliveries/<int:delivery_id>/` – страница поставки (view-функция `delivery_detail()`);
* `/suppliers/` – список поставщиков: объекты `Supplier` из `data/suppliers.json` (view-функция `suppliers_list()`);
* `/suppliers/<int:supplier_id>/` – страница поставщика (view-функция `supplier_detail()`);
* `/products/` – список товаров: объекты `Product` из `data/products.json` (view-функция `products_list()`);
* `/products/<int:product_id>/` – страница товара (view-функция `product_detail()`).

Если поставка, поставщик или товар с указанным идентификатором не найдены,
соответствующая страница возвращает код статуса 404.

## Веб-интерфейс

Веб-часть приложения реализована на Django.

Для формирования страниц используются Django-шаблоны.

Генерация HTML непосредственно в Python-коде веб-представлений не используется.
Функция `page()` больше не используется веб-представлениями.

Представления подготавливают данные и передают их в шаблоны через контекст.

## Django Template Language

Шаблоны используют возможности Django Template Language.

### Базовый шаблон

Общий шаблон страниц: `templates/base.html`

Он содержит общую HTML-структуру страницы, подключение стилей и JavaScript,
навигацию и блоки для содержимого отдельных страниц.

Дочерние шаблоны используют наследование:
`{% extends "base.html" %}`

Содержимое отдельных страниц размещается в блоке:
`{% block content %}{% endblock %}`

Заголовок страницы задаётся через блок:
`{% block title %}{% endblock %}`

### Включаемые шаблоны

Повторяющиеся фрагменты вынесены в отдельные шаблоны.

Для поставок используются:
* `deliveries/includes/delivery_card.html`
* `deliveries/includes/delivery_status.html`

Для поставщиков используется:
* `suppliers/includes/supplier_card.html`

Для товаров используется:
* `products/includes/product_card.html`

Подключение выполняется с помощью:
`{% include "deliveries/includes/delivery_card.html" %}`

### Контекст

Представления передают данные в шаблоны через словарь контекста.

Например, для списка поставок:
`context = {"deliveries": deliveries_list}`

В шаблоне данные доступны по имени переменной:
`{% for delivery in deliveries %}`

Для страницы отдельной поставки используется переменная:
`{{ delivery }}`

### Циклы и условия

Для формирования списков используются циклы:
`{% for delivery in deliveries %}`

При отсутствии элементов используется:
`{% empty %}`

Условия используются для отображения различного содержимого страницы и статуса поставки:
`{% if delivery.is_cancelled %}`

## Фильтры шаблонов

В шаблонах используются стандартные фильтры Django Template Language.

Количество элементов:
`{{ deliveries|length }}`

Для отображения значения по умолчанию:
`{{ supplier.name|default:"Без названия" }}`

Фильтры используются для представления данных и не содержат бизнес-логику приложения.

Дата поставки на текущем этапе хранится как строковое значение и выводится без преобразования средствами шаблона.

## URL-маршрутизация

Для страниц используются именованные маршруты Django.

Примеры:
* `{% url 'deliveries:list' %}`
* `{% url 'deliveries:detail' delivery.id %}`
* `{% url 'suppliers:list' %}`
* `{% url 'suppliers:detail' supplier.id %}`
* `{% url 'products:list' %}`
* `{% url 'products:detail' product.id %}`

Для приложений используются пространства имён (namespace), что позволяет обращаться к маршрутам через имена вида:
* `deliveries:list`
* `deliveries:detail`
* `suppliers:list`
* `suppliers:detail`
* `products:list`
* `products:detail`

Ссылки в шаблонах формируются через `{% url %}`, а не за счёт жёстко заданных адресов.

## Статические файлы

Статические файлы проекта находятся в каталоге:
`homepage/static/homepage/`

Используются:
* `css/style.css`
* `js/main.js`
* `img/logo.png`

Для работы со статическими файлами в шаблонах используется:
`{% load static %}`

CSS подключается через:
`{% static 'homepage/css/style.css' %}`

Изображение:
`{% static 'homepage/img/logo.png' %}`

JavaScript:
`{% static 'homepage/js/main.js' %}`

В проекте используется собственный CSS для оформления элементов интерфейса.

JavaScript используется для небольшого динамического поведения интерфейса, в том числе для автоматического отображения текущего года в нижней части страницы.

## Хранение данных

Данные приложения хранятся в JSON-файлах:
* `data/suppliers.json`;
* `data/products.json`;
* `data/deliveries.json`.

При загрузке данные из JSON преобразуются в объекты `Supplier`, `Product` и `Delivery`.

При сохранении объекты преобразуются в данные JSON.

Для связи поставки с поставщиком и товаром в `deliveries.json` используются их
идентификаторы `supplier_id` и `product_id`.

Django ORM на текущем этапе не используется.

## Структура проекта

```text
supply-tracker/
├── manage.py                 # точка входа Django
├── main.py                   # консольная версия приложения (ПР3)
├── storage.py                # загрузка и сохранение JSON (ПР3)
├── utils.py                  # функции безопасного ввода (ПР3)
├── conftest.py               # конфигурация pytest (корень проекта в sys.path)
├── requirements.txt
├── README.md
├── .flake8
├── .gitignore
│
├── supplytracker/            # пакет настроек Django-проекта
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/                # шаблоны уровня проекта
│   ├── base.html
│   ├── 404.html
│   ├── 500.html
│   └── includes/
│       └── navigation.html
│
├── homepage/                 # приложение: главная страница и статика
│   ├── migrations/
│   ├── static/
│   │   └── homepage/
│   │       ├── css/style.css
│   │       ├── js/main.js
│   │       └── img/logo.png
│   ├── templates/
│   │   └── homepage/
│   │       └── index.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── deliveries/               # приложение: поставки
│   ├── migrations/
│   ├── templates/
│   │   └── deliveries/
│   │       ├── delivery_list.html
│   │       ├── delivery_detail.html
│   │       ├── available.html
│   │       ├── statistics.html
│   │       └── includes/
│   │           └── delivery_status.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── suppliers/                # приложение: поставщики
│   ├── migrations/
│   ├── templates/
│   │   └── suppliers/
│   │       ├── supplier_list.html
│   │       └── supplier_detail.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── products/                 # приложение: товары
│   ├── migrations/
│   ├── templates/
│   │   └── products/
│   │       ├── product_list.html
│   │       └── product_detail.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── models/                   # классы предметной области (ПР3)
│   ├── __init__.py
│   ├── suppliers.py
│   ├── products.py
│   └── deliveries.py
│
├── db/                       # слой подключения к SQLite (ПР7)
│   ├── __init__.py
│   ├── database.py
│   └── import_json.py
│
├── sql/                      # SQL-скрипты проекта (ПР7)
│   ├── schema.sql
│   └── queries.sql
│
├── data/                     # данные приложения
│   ├── suppliers.json
│   ├── products.json
│   ├── deliveries.json
│   └── supplytracker.sqlite
│
└── tests/                    # автоматизированные тесты pytest
    ├── __init__.py
    ├── test_suppliers.py
    ├── test_products.py
    └── test_deliveries.py

### Структура базы данных

Три таблицы, связанные внешними ключами:

| Таблица | Поля | Ключи |
|---------|------|-------|
| `suppliers` | `id INTEGER`, `name TEXT` | `PRIMARY KEY (id)` |
| `products` | `id INTEGER`, `name TEXT`, `price REAL` | `PRIMARY KEY (id)` |
| `deliveries` | `id INTEGER`, `supplier_id INTEGER`, `product_id INTEGER`, `quantity INTEGER`, `delivery_date TEXT`, `is_paid INTEGER`, `is_cancelled INTEGER` | `PRIMARY KEY (id)`, `FOREIGN KEY (supplier_id) REFERENCES suppliers(id)`, `FOREIGN KEY (product_id) REFERENCES products(id)` |

### Файлы слоя БД

- `sql/schema.sql` — SQL-скрипт создания таблиц;
- `sql/queries.sql` — SQL-запросы проекта (13 запросов);
- `db/database.py` — модуль подключения к SQLite (включает `PRAGMA foreign_keys = ON`);
- `db/import_json.py` — скрипт однократного переноса данных из JSON;
- `data/supplytracker.sqlite` — файл базы данных.

### SQL-запросы проекта

В `sql/queries.sql` реализованы запросы всех требуемых видов:

| № | Тип | Назначение |
|---|-----|-----------|
| 1 | SELECT | Список всех поставщиков |
| 2 | SELECT + WHERE | Список товаров дороже 20 руб. |
| 3 | SELECT + WHERE | Список активных поставок |
| 4 | SELECT + WHERE | Список отменённых поставок |
| 5 | JOIN | Полная информация о поставках (3 таблицы) |
| 6 | JOIN + WHERE | Поставки конкретного поставщика |
| 7 | GROUP BY | Количество поставок по статусам |
| 8 | LEFT JOIN + GROUP BY | Количество поставок по поставщикам |
| 9 | JOIN + SUM + GROUP BY | Общая стоимость по поставщикам |
| 10 | JOIN + GROUP BY + HAVING | Поставщики с более чем 1 активной поставкой |
| 11 | NOT IN + параметр `?` | Поиск поставок, не принятых на выбранную дату |
| 12 | ORDER BY + LIMIT | Топ-3 самых дорогих товаров |
| 13 | LEFT JOIN + IS NULL | Товары, по которым не было активных поставок |

### Django-интеграция

- В представлениях используется `sqlite3.Row` для доступа к полям по именам;
- Значения передаются параметрами `?` (безопасные параметризованные запросы);
- Результаты запросов передаются в шаблоны через `context`.

### Страницы с данными из SQLite

- `/deliveries/` — список поставок (JOIN трёх таблиц);
- `/deliveries/available/` — поиск по дате (NOT IN + параметр);
- `/deliveries/statistics/` — статистика (GROUP BY + SUM);
- `/suppliers/` — список поставщиков;
- `/products/` — список товаров.

### Импорт данных

Перед первым запуском веб-интерфейса импортируйте данные:

```bash
python -m db.import_json