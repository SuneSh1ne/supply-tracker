"""Точка запуска приложения."""
from typing import List

from models import Supplier, Product, Delivery
from models.suppliers import add_supplier, find_supplier_by_id, show_suppliers
from models.products import add_product, find_product_by_id, show_products
from models.deliveries import (
    add_delivery, find_delivery, filter_deliveries_by_status,
    sort_deliveries_by_date, show_deliveries
)
from storage import (
    load_suppliers, save_suppliers,
    load_products, save_products,
    load_deliveries, save_deliveries
)
from utils import input_int, input_float, input_date, input_yes_no


def show_delivery_details(delivery: Delivery) -> None:
    """Вывести подробную информацию о поставке."""
    print("\n--- Детали поставки ---")
    print(f"ID: {delivery.id}")
    print(f"Поставщик: {delivery.supplier.name}")
    print(f"Товар: {delivery.product.name}")
    print(f"Количество: {delivery.quantity} шт.")
    print(f"Цена за единицу: {delivery.product.price:.2f} руб.")
    print(f"Итоговая стоимость: {delivery.calculate_total_cost():.2f} руб.")
    print(f"Дата поставки: {delivery.delivery_date}")
    print(f"Оплачено: {'Да' if delivery.is_paid else 'Нет'}")
    print(f"Статус: {delivery.get_status()}\n")


def main() -> None:
    """Главный цикл приложения."""
    suppliers: List[Supplier] = load_suppliers()
    products: List[Product] = load_products()
    deliveries: List[Delivery] = load_deliveries(suppliers, products)

    while True:
        print("\n=== Система учёта поставок ===")
        print("1. Показать все поставки")
        print("2. Добавить новую поставку")
        print("3. Найти поставку")
        print("4. Показать поставки по статусу")
        print("5. Показать поставки по дате")
        print("6. Управление поставщиками")
        print("7. Управление товарами")
        print("8. Отменить поставку")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_deliveries(deliveries)

        elif choice == "2":
            if not suppliers:
                print("Сначала добавьте поставщика (пункт 6).")
                continue
            if not products:
                print("Сначала добавьте товар (пункт 7).")
                continue

            show_suppliers(suppliers)
            sup_id = input_int("Введите ID поставщика: ")
            supplier = find_supplier_by_id(suppliers, sup_id)
            if not supplier:
                print("Поставщик не найден.")
                continue

            show_products(products)
            prod_id = input_int("Введите ID товара: ")
            product = find_product_by_id(products, prod_id)
            if not product:
                print("Товар не найден.")
                continue

            quantity = input_int("Количество: ")
            date_str = input_date("Дата поставки (ДД.ММ.ГГГГ): ")
            is_paid = input_yes_no("Оплачено? (да/нет): ")

            delivery = add_delivery(deliveries, supplier, product, quantity, date_str, is_paid)
            if delivery:
                print(f"Поставка #{delivery.id} успешно добавлена.")
                save_deliveries(deliveries)

        elif choice == "3":
            query = input("Введите строку для поиска: ").strip()
            found = find_delivery(deliveries, query)
            if found:
                for d in found:
                    show_delivery_details(d)
            else:
                print("Поставки не найдены.")

        elif choice == "4":
            print("Статусы:")
            print("  'Поставка принята на склад'")
            print("  'Поставка ожидает оплаты'")
            print("  'Поставка отменена'")
            print("  'Поставка отклонена: некорректное количество'")
            status = input("Введите статус: ").strip()
            filtered = filter_deliveries_by_status(deliveries, status)
            show_deliveries(filtered)

        elif choice == "5":
            show_deliveries(sort_deliveries_by_date(deliveries))

        elif choice == "6":
            print("\n-- Поставщики --")
            show_suppliers(suppliers)
            name = input("Название нового поставщика (или Enter для отмены): ").strip()
            if name:
                s = add_supplier(suppliers, name)
                print(f"Поставщик {s.name} добавлен.")
                save_suppliers(suppliers)

        elif choice == "7":
            print("\n-- Товары --")
            show_products(products)
            name = input("Название нового товара (или Enter для отмены): ").strip()
            if name:
                price = input_float("Цена за единицу: ")
                if Product.validate_price(price):
                    p = add_product(products, name, price)
                    print(f"Товар {p.name} добавлен.")
                    save_products(products)
                else:
                    print("Ошибка: цена должна быть больше 0.")

        elif choice == "8":
            show_deliveries(deliveries)
            d_id = input_int("Введите ID поставки для отмены: ")
            delivery = next((d for d in deliveries if d.id == d_id), None)
            if delivery:
                if delivery.is_cancelled:
                    print("Эта поставка уже отменена.")
                else:
                    delivery.cancel()
                    print(f"Поставка #{delivery.id} отменена.")
                    save_deliveries(deliveries)
            else:
                print("Поставка не найдена.")

        elif choice == "0":
            print("Сохранение данных и выход...")
            save_suppliers(suppliers)
            save_products(products)
            save_deliveries(deliveries)
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()