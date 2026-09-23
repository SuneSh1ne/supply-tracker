"""Точка запуска приложения и основной сценарий взаимодействия."""
from typing import List, Dict, Any

from deliveries import (
    add_delivery,
    find_delivery,
    filter_deliveries_by_status,
    sort_deliveries_by_date,
    validate_delivery,
)
from storage import load_deliveries, save_deliveries
from utils import input_int, input_float, input_date, input_yes_no


def show_deliveries(deliveries: List[Dict[str, Any]]) -> None:
    """Вывести список всех поставок в виде таблицы."""
    if not deliveries:
        print("Список поставок пуст.")
        return
    
    header = "{:<5} | {:<20} | {:<25} | {:<8} | {:<10} | {:<12} | {:<25}"
    print(header.format("ID", "Поставщик", "Товар", "Кол-во", "Цена", "Стоимость", "Статус"))
    print("-" * 115)
    for d in deliveries:
        print(header.format(
            d["id"], d["supplier_name"][:20], d["product_name"][:25], 
            d["quantity"], d["price"], d["total_cost"], d["status"]
        ))
    print()


def show_delivery_details(delivery: Dict[str, Any]) -> None:
    """Вывести подробную информацию о поставке."""
    print("\n--- Детали поставки ---")
    print(f"ID: {delivery['id']}")
    print(f"Поставщик: {delivery['supplier_name']}")
    print(f"Товар: {delivery['product_name']}")
    print(f"Количество: {delivery['quantity']} шт.")
    print(f"Цена за единицу: {delivery['price']:.2f} руб.")
    print(f"Итоговая стоимость: {delivery['total_cost']:.2f} руб.")
    print(f"Дата поставки: {delivery['delivery_date']}")
    print(f"Оплачено: {'Да' if delivery['is_paid'] else 'Нет'}")
    print(f"Статус: {delivery['status']}\n")


def main() -> None:
    """Точка запуска приложения."""
    deliveries = load_deliveries()
    
    # Генерация следующего ID с использованием генератора (расширенная возможность Python)
    next_id = max((d["id"] for d in deliveries), default=0) + 1

    while True:
        print("\n=== Система учёта поставок ===")
        print("1. Показать все поставки")
        print("2. Добавить новую поставку")
        print("3. Найти поставку по названию")
        print("4. Показать поставки по статусу")
        print("5. Показать поставки, отсортированные по дате")
        print("0. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            show_deliveries(deliveries)
        elif choice == "2":
            supplier = input("Название поставщика: ").strip()
            product = input("Название товара: ").strip()
            quantity = input_int("Количество: ")
            price = input_float("Цена за единицу: ")
            date_str = input_date("Дата поставки (ДД.ММ.ГГГГ): ")
            is_paid = input_yes_no("Оплачено? (да/нет): ")
            
            if not validate_delivery(supplier, product, quantity, price):
                print("Ошибка: некорректные данные поставки (проверьте названия, количество и цену > 0).")
                continue
                
            add_delivery(deliveries, next_id, supplier, product, quantity, price, date_str, is_paid)
            print(f"Поставка с ID {next_id} успешно добавлена.")
            next_id += 1
            save_deliveries(deliveries)
        elif choice == "3":
            query = input("Введите строку для поиска (поставщик или товар): ").strip()
            found = find_delivery(deliveries, query)
            if found:
                print(f"\nНайдено поставок: {len(found)}")
                for d in found:
                    show_delivery_details(d)
            else:
                print("Поставки не найдены.")
        elif choice == "4":
            print("Доступные статусы: 'Поставка принята на склад', 'Поставка ожидает оплаты', 'Поставка отклонена: некорректные данные'")
            status = input("Введите статус для фильтрации: ").strip()
            filtered = filter_deliveries_by_status(deliveries, status)
            if filtered:
                show_deliveries(filtered)
            else:
                print("Поставки с таким статусом не найдены.")
        elif choice == "5":
            sorted_deliveries = sort_deliveries_by_date(deliveries)
            show_deliveries(sorted_deliveries)
        elif choice == "0":
            print("Сохранение данных и выход...")
            save_deliveries(deliveries)
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()