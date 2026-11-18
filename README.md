# Supply Tracker — сервис учёта поставок

Консольное и веб-приложение для учёта поступлений товаров на склад от поставщиков.
Проект развивается поэтапно: консольная версия дополнена веб-интерфейсом на Django,
слой данных прошёл путь от JSON до SQLite и Django ORM, настроена административная
панель Django и анализ SQL-запросов.

## 1. Назначение проекта

Supply Tracker — учебное приложение для складской логистики.

Приложение позволяет:
* просматривать поставки, поставщиков и товары в браузере;
* просматривать подробную информацию о поставке, поставщике и товаре;
* искать поставки по названию поставщика или товара;
* фильтровать поставки по дате, поставщику, товару и цене товара;
* сортировать список поставок по дате, поставщику, товару и количеству;
* просматривать поставки постранично с сохранением параметров фильтрации;
* искать поставки и свободных поставщиков на выбранную дату;
* просматривать статистику количества и стоимости поставок по поставщикам;
* рассчитывать итоговую стоимость поставки;
* отслеживать статус поставки (активна / ожидает оплаты / отменена / завершена);
* управлять справочниками и поставками через административную панель Django;
* добавлять поставки, поставщиков и товары, отменять поставки (консольная версия и админ-панель);
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
* Django Debug Toolbar — анализ SQL-запросов в режиме разработки;
* Unidecode — транслитерация названий для формирования slug;
* JSON — историческое хранилище данных (ПР2–ПР6);
* Git, pytest, flake8.

## 3. Предметная область

Основные объекты предметной области:
* поставщик;
* товар;
* поставка.

Поставка связывает поставщика и товар: фиксирует факт поступления определённого
количества товара от конкретного поставщика на указанную дату.
Одна поставка относится к одному поставщику и одному товару;
один поставщик и один товар могут участвовать в нескольких поставках.

Правила работы со статусами:
* отменённая и завершённая поставка не удаляется из системы — запись сохраняется как история;
* отменённые и завершённые поставки не учитываются как активные: они не попадают
  в выборки активных поставок, не блокируют поставщика при поиске по дате
  и не участвуют в статистике активных поставок.

## 4. Основные сущности

### Supplier — поставщик

Консольный класс (`models/suppliers.py`) и модель Django (`suppliers/models.py`).

Поля модели:
* `id` — первичный ключ;
* `name` — название поставщика (`CharField`).

Обратная связь: `supplier.deliveries.all()` — поставки поставщика
(`related_name="deliveries"`).

### Product — товар

Консольный класс (`models/products.py`) и модель Django (`products/models.py`).

Поля модели:
* `id` — первичный ключ;
* `name` — название товара (`CharField`);
* `price` — цена за единицу (`DecimalField`, с подсказкой `help_text`);
* `is_expensive` — вычисляемое поле (`GeneratedField`): признак «дорогой товар»
  (цена не менее 1000 руб.); значение вычисляется и хранится на стороне базы данных
  и автоматически пересчитывается при изменении цены;
* `slug` — уникальный URL-идентификатор (`SlugField`, `editable=False`), формируется
  автоматически транслитерацией названия (Unidecode + `slugify`) с добавлением первичного ключа.

Методы модели:
* `save()` — автоматическое формирование slug для новых объектов;
* `get_absolute_url()` — адрес страницы товара (`/products/<slug>/`);
* `__str__()` — строковое представление.

### Delivery — поставка

Консольный класс (`models/deliveries.py`) и модель Django (`deliveries/models.py`).

Поля модели:
* `id` — первичный ключ;
* `supplier` — внешний ключ на `Supplier` (`on_delete=PROTECT`, `related_name="deliveries"`);
* `product` — внешний ключ на `Product` (`on_delete=PROTECT`, `related_name="deliveries"`);
* `quantity` — количество единиц товара (`PositiveIntegerField`);
* `delivery_date` — дата поставки (`DateField`);
* `is_paid` — признак оплаты (`BooleanField`);
* `status` — статус поставки (`CharField` с `TextChoices`):
  * `ACTIVE` — активна;
  * `CANCELLED` — отменена;
  * `COMPLETED` — завершена.

Методы модели:
* `calculate_total_cost()` — расчёт итоговой стоимости поставки;
* `cancel()` — отмена поставки (переход в статус `CANCELLED`);
* `complete()` — завершение поставки (переход в статус `COMPLETED`);
* `__str__()` — строковое представление.

Параметр `on_delete=PROTECT` запрещает удаление поставщика или товара,
на которых ссылаются поставки: история поставок сохраняется.

Менеджер записей:
* `DeliveryQuerySet` — набор запросов с методами `active()`, `cancelled()`,
  `completed()`, `for_date(date)`;
* `DeliveryManager` — менеджер модели на основе `DeliveryQuerySet`, подключён как
  `Delivery.objects`; обычный `Delivery.objects.all()` по-прежнему возвращает все
  записи, включая отменённые и завершённые.

## 5. Страницы веб-интерфейса

| Страница | URL | View-функция | Источник данных |
|----------|-----|--------------|-----------------|
| Главная | `/` | `homepage.views.index` | контекстный процессор |
| Список поставок | `/deliveries/` | `deliveries.views.deliveries_list` | ORM: фильтры, поиск, сортировка, пагинация |
| Поиск по дате | `/deliveries/available/` | `deliveries.views.available_deliveries` | ORM: менеджер `active()`, `for_date()`, `exclude()` |
| Статистика | `/deliveries/statistics/` | `deliveries.views.statistics` | ORM: `annotate`, `Count`, `Sum`, `Coalesce` |
| Поставка | `/deliveries/<int:delivery_id>/` | `deliveries.views.delivery_detail` | ORM: `get_object_or_404`, `select_related` |
| Список поставщиков | `/suppliers/` | `suppliers.views.suppliers_list` | ORM: `all()` |
| Поставщик | `/suppliers/<int:supplier_id>/` | `suppliers.views.supplier_detail` | ORM: `get_object_or_404` |
| Список товаров | `/products/` | `products.views.products_list` | ORM: `all()` |
| Товар | `/products/<slug:slug>/` | `products.views.product_detail` | ORM: `get_object_or_404` по slug |

Если объект с указанным идентификатором или slug не найден, возвращается код
статуса 404 и собственная страница ошибки (`templates/404.html`);
внутренние ошибки отображаются через `templates/500.html`.

## 6. Административная панель (ПР10)

Панель доступна по адресу `/admin/` после создания суперпользователя
(`python manage.py createsuperuser`).

Зарегистрированы все модели предметной области:

* `SupplierAdmin` — столбцы списка (включая счётчик активных поставок, вычисленный
  аннотацией `Count` с условием `Q`), поиск по названию, сортировка, постраничный
  вывод, поле `id` только для чтения, встроенная таблица поставок (`TabularInline`);
* `ProductAdmin` — столбцы списка (включая вычисляемое поле `is_expensive`),
  редактирование цены прямо в списке (`list_editable`), поиск по названию,
  встроенная таблица поставок, ссылка «Посмотреть на сайте» (`view_on_site`)
  на основе `get_absolute_url()`;
* `DeliveryAdmin` — столбцы со связанными поставщиком и товаром и ценой товара,
  поиск по полям связанных моделей (`supplier__name`, `product__name`),
  фильтры по дате, статусу и оплате, навигация по датам (`date_hierarchy`),
  автодополнение при выборе поставщика и товара (`autocomplete_fields`),
  оптимизация списка (`list_select_related`), массовые действия
  «Отменить выбранные поставки» и «Вернуть в активные».

Разграничение доступа проверено отдельной группой с разрешениями
просмотра/добавления/изменения товаров без права удаления; учётная запись группы
не является суперпользователем. Удаление поставщика или товара, на которых
ссылаются поставки, запрещено на уровне модели (`on_delete=PROTECT`).

Административная панель не заменяет бизнес-логику приложения: правила предметной
области реализованы в моделях и менеджере запросов.

## 7. Слой данных и его развитие

| Этап | Хранилище и доступ |
|------|--------------------|
| ПР2–ПР6 | JSON-файлы `data/*.json`, загрузка функциями `storage.py` |
| ПР7 | SQLite `data/supplytracker.sqlite`: `sql/schema.sql`, `sql/queries.sql`, `db/database.py`, `db/import_json.py`, представления через `sqlite3.Row` |
| ПР9 | Django ORM: модели, миграции, целевая база `db.sqlite3`, перенос данных `db/import_sqlite_to_orm.py` |
| ПР10 | Миграция статусов (`is_cancelled` → `status`), `GeneratedField`, `slug`, админ-панель, Debug Toolbar |

Файлы SQL-слоя ПР7 (`sql/schema.sql`, `sql/queries.sql`, `db/database.py`,
`db/import_json.py`) сохранены в репозитории как предыдущая реализация предметной
области; представления после ПР9 их не используют.

Перенос данных между хранилищами:
* `db/inspect_source_db.py` — инспекция исходной базы ПР7 (таблицы, столбцы, количество записей);
* `db/import_sqlite_to_orm.py` — перенос данных из `data/supplytracker.sqlite` в базу Django
  (`update_or_create`, `transaction.atomic`, сохранение первичных ключей и связей,
  преобразование строк дат `ДД.ММ.ГГГГ` в объекты `date`).

Изменения структуры базы данных оформлены миграциями; файлы миграций хранятся в Git.
Локальные базы данных (`db.sqlite3`, резервные копии) в репозиторий не включаются.

## 8. Используемые ORM-запросы

| Категория | Примеры в проекте |
|-----------|-------------------|
| Получение наборов | `all()`, `filter()`, `exclude()`, `order_by()` |
| Получение одного объекта | `get_object_or_404(..., pk=...)`, `get_object_or_404(..., slug=...)` |
| Фильтрация по связанной модели | `filter(product__price__gte=...)`, `filter(supplier_id=...)` |
| Поиск | `supplier__name__icontains`, `Q(...) \| Q(product__name__icontains=...)` |
| Сортировка | `order_by(sort_field, "id")` через словарь разрешённых полей `SORT_FIELDS` |
| Связи | `select_related("supplier", "product")`, обратная связь `supplier.deliveries` |
| Менеджер и QuerySet | `Delivery.objects.active()`, `.cancelled()`, `.completed()`, `.for_date(date)` |
| Агрегирование | `Count("deliveries", filter=Q(...))`, `Sum(F(...) * F(...), filter=Q(...))`, `Coalesce`, `count()` |
| Аннотирование | `annotate(supplier_name=F("name"), deliveries_count=..., total_cost=...)` |
| Постраничный вывод | `Paginator`, `get_page()`, навигация через `{% querystring %}` |

Безопасность запросов: поле сортировки выбирается через словарь разрешённых
соответствий, произвольный пользовательский ввод в `order_by()` не передаётся;
даты и числа из параметров запроса проверяются и преобразуются до использования.

## 9. Шаблоны, статические файлы и контекстный процессор

* базовый шаблон `templates/base.html` с блоками `{% block title %}` и `{% block content %}`;
* навигация вынесена в `templates/includes/navigation.html` и подключается через `{% include %}`;
* дочерние шаблоны наследуют базовый через `{% extends "base.html" %}`;
* повторяющиеся фрагменты вынесены во включаемые шаблоны
  (например, `deliveries/includes/delivery_status.html`);
* данные передаются из представлений через контекст; в шаблонах используются
  циклы `{% for %}`, условия `{% if %}`, `{% empty %}`, фильтры
  (`length`, `default`, `date`, `floatformat`);
* ссылки формируются через именованные маршруты `{% url %}` с пространствами имён
  и через `get_absolute_url()`;
* пагинация сохраняет параметры запроса через `{% querystring %}`;
* контекстный процессор `homepage/context_processors.py` (`site_context`) передаёт
  во все шаблоны название сайта и счётчики сущностей
  (`site_name`, `suppliers_count`, `products_count`, `deliveries_count`);
  процессор зарегистрирован в `TEMPLATES` файла `settings.py`, счётчики отображаются
  в навигации и подвале;
* статические файлы приложения `homepage`: `css/style.css`, `js/main.js`
  (вывод текущего года в подвале), `img/logo.png`; подключаются через
  `{% load static %}` и `{% static %}`.

## 10. Структура проекта

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
├── homepage/                  # приложение: главная страница, статика, контекст
│   ├── migrations/
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── templates/homepage/
│   │   └── index.html
│   ├── context_processors.py
│   ├── urls.py
│   └── views.py
├── deliveries/                # приложение: поставки
│   ├── migrations/
│   ├── templates/deliveries/
│   │   ├── delivery_list.html
│   │   ├── delivery_detail.html
│   │   ├── available.html
│   │   ├── statistics.html
│   │   └── includes/
│   │       └── delivery_status.html
│   ├── admin.py
│   ├── models.py              # модель Delivery, DeliveryQuerySet, DeliveryManager
│   ├── urls.py
│   └── views.py
├── suppliers/                 # приложение: поставщики
│   ├── migrations/
│   ├── templates/suppliers/
│   │   ├── supplier_list.html
│   │   └── supplier_detail.html
│   ├── admin.py
│   ├── models.py              # модель Supplier
│   ├── urls.py
│   └── views.py
├── products/                  # приложение: товары
│   ├── migrations/
│   ├── templates/products/
│   │   ├── product_list.html
│   │   └── product_detail.html
│   ├── admin.py
│   ├── models.py              # модель Product (slug, GeneratedField)
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
│   └── supplytracker.sqlite   # исходная база ПР7 (не в репозитории)
├── tests/                     # автоматизированные тесты pytest
│   ├── __init__.py
│   ├── test_suppliers.py
│   ├── test_products.py
│   └── test_deliveries.py
└── db.sqlite3                 # целевая база Django (не в репозитории)
```

## 11. Назначение основных модулей

* `main.py` — консольная версия приложения: меню и пользовательские сценарии;
* `models/` — классы предметной области ПР3 и функции работы с коллекциями;
* `storage.py` — преобразование JSON ↔ объекты Python;
* `utils.py` — безопасный консольный ввод чисел, дат и ответов «да/нет»;
* `supplytracker/` — настройки проекта, корневая маршрутизация, точки входа серверов;
* `homepage/`, `deliveries/`, `suppliers/`, `products/` — Django-приложения:
  модели, представления, маршруты, шаблоны и настройки админ-панели;
* `homepage/context_processors.py` — общие данные для всех шаблонов;
* `db/` — скрипты подключения, инспекции и переноса данных между хранилищами;
* `sql/` — схема базы и SQL-запросы предыдущей реализации (ПР7);
* `tests/` — тесты классов предметной области.

## 12. Запуск проекта

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/SuneSh1ne/supply-tracker.git
   cd supply-tracker
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv venv
   source venv/Scripts/activate      # Git Bash (Windows)
   # venv\Scripts\activate           # PowerShell / cmd (Windows)
   # source venv/bin/activate        # Linux / macOS
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Примените миграции:

   ```bash
   python manage.py migrate
   ```

5. Наполните базу данными (раздел 13).

6. Запустите сервер разработки:

   ```bash
   python manage.py runserver --insecure
   ```

   Флаг `--insecure` необходим, потому что в проекте отключён отладочный режим
   (`DEBUG = False`), а статические файлы на этапе разработки раздаёт development-сервер.

7. Откройте в браузере: `http://127.0.0.1:8000/`

Консольная версия (сохранена с ПР3):

```bash
python main.py
```

## 13. Наполнение базы данных

База `db.sqlite3` в репозиторий не включается: после клонирования таблицы создаются
миграциями, а данные наполняются переносом из исходных файлов.

Вариант 1 — перенос из базы ПР7 (если файл `data/supplytracker.sqlite` присутствует):

```bash
python db/import_sqlite_to_orm.py
```

Вариант 2 — полный путь от JSON (создание базы ПР7 и перенос в ORM):

```bash
python -c "import sqlite3; sqlite3.connect('data/supplytracker.sqlite').close()"
python -c "import sqlite3; conn=sqlite3.connect('data/supplytracker.sqlite'); sql=open('sql/schema.sql', encoding='utf-8').read(); conn.executescript(sql); conn.commit(); conn.close()"
python -m db.import_json
python db/import_sqlite_to_orm.py
```

Проверка переноса:

```bash
python manage.py shell
```

```python
from suppliers.models import Supplier
from products.models import Product
from deliveries.models import Delivery
print(Supplier.objects.count(), Product.objects.count(), Delivery.objects.count())
print(Delivery.objects.active().count(), Delivery.objects.cancelled().count())
```

## 14. Административная панель: первый вход

```bash
python manage.py createsuperuser
python manage.py runserver --insecure
```

Откройте `http://127.0.0.1:8000/admin/` и войдите под созданной учётной записью.

Анализ SQL-запросов (Django Debug Toolbar) выполняется только в режиме разработки:
панель подключена условно и отображается при временно включённом `DEBUG = True`.
В обычном состоянии проекта `DEBUG = False`, поэтому панель скрыта — это требуемое
поведение для учебного «боевого» режима.

## 15. Тестирование

```bash
pytest -v
```

Тесты проверяют создание объектов предметной области, значения атрибутов,
строковые представления, методы классов (`calculate_total_cost`, `cancel`,
`validate_price`), добавление объектов в коллекции и связи между ними.

## 16. Проверка качества кода

```bash
flake8 . --extend-exclude=venv
python manage.py check
python manage.py showmigrations
python manage.py makemigrations --check
```

## 17. Зависимости

Состав `requirements.txt`:
* `Django==5.2.*` — веб-фреймворк;
* `pytest` — автоматизированные тесты;
* `flake8` — проверка качества кода;
* `django-debug-toolbar` — анализ SQL-запросов в режиме разработки;
* `Unidecode` — транслитерация названий при формировании slug.

## 18. Работа с Git

Исходный код проекта хранится в Git-репозитории.
Изменения каждой практической работы фиксируются коммитами с метками этапа
(`PR3:`, `PR5:`, `PR6:`, `PR7:`, `PR9:`, `PR10:`).
Локальные базы данных и резервные копии исключены из репозитория через `.gitignore`.

## 19. Текущее состояние проекта

Реализовано:
* предметные классы ПР3 и консольный интерфейс;
* хранение данных в JSON (исторический этап), SQLite (ПР7) и Django ORM (ПР9);
* Django-проект с четырьмя приложениями;
* шаблоны Django, наследование, включаемые шаблоны, фильтры, статические файлы;
* собственные страницы ошибок 404 и 500;
* модели Django со связями `ForeignKey` (`on_delete=PROTECT`, `related_name`), миграции;
* перенос данных между хранилищами без потери связей;
* ORM-запросы: фильтрация, поиск, сортировка, агрегирование, пагинация;
* пользовательский менеджер и QuerySet поставок (`active`, `cancelled`, `completed`, `for_date`);
* статусы поставок на `TextChoices` с миграцией данных из `is_cancelled`;
* вычисляемое поле `GeneratedField` и slug с `get_absolute_url()` у товара;
* контекстный процессор с общими данными для шаблонов;
* административная панель Django: регистрация моделей, `ModelAdmin`, inline-формы,
  массовые действия, `date_hierarchy`, `autocomplete_fields`, проверка прав доступа;
* анализ SQL-запросов через Django Debug Toolbar;
* страницы списков, карточек, поиска по дате и статистики;
* тесты предметной области; проверка кода `flake8`.

Не реализовано (планируется):
* формы Django для создания и редактирования объектов через веб-интерфейс (POST-сценарии);
* регистрация и аутентификация пользователей сайта;
* API, контейнеризация, CI/CD.

## 20. Дальнейшее развитие

* реализация форм Django и POST-сценариев (создание, изменение, отмена поставок);
* расширение статистики и отчётов;
* разработка API;
* контейнеризация приложения и настройка CI/CD.
