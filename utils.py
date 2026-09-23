"""Вспомогательные функции для безопасного ввода данных пользователем."""
from datetime import datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    """Запросить у пользователя число с плавающей точкой."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число.")


def input_date(prompt: str) -> str:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        date_str = input(prompt)
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            return date_str
        except ValueError:
            print("Ошибка: формат ДД.ММ.ГГГГ.")


def input_yes_no(prompt: str) -> bool:
    """Запросить у пользователя ответ Да/Нет."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("да", "y", "yes"):
            return True
        if choice in ("нет", "n", "no"):
            return False
        print("Ошибка: введите 'да' или 'нет'.")