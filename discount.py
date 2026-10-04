"""Модуль расчёта скидки."""
from datetime import datetime, timedelta
import sqlite3
from databases.config import DB_PATH


def get_previous_month_range(date):
    """
    Возвращает (начало, конец) предыдущего месяца.

    :param date: дата расчёта
    :return: (start_date, end_date) в формате YYYY-MM-DD
    """
    first_day = date.replace(day=1)                 # 1-е число текущего месяца
    last_day_prev = first_day - timedelta(days=1)   # последний день прошлого месяца
    first_day_prev = last_day_prev.replace(day=1)   # 1-е число прошлого месяца
    return (
        first_day_prev.strftime("%Y-%m-%d"),
        last_day_prev.strftime("%Y-%m-%d")
    )


def has_orders_in_previous_month(product_id, date):
    """
    Есть ли заказы товара в предыдущем месяце?

    :param product_id: id товара
    :param date: дата расчёта
    :return: True / False
    """
    start, end = get_previous_month_range(date)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM Заказ "
        "WHERE товар_id = ? AND дата BETWEEN ? AND ?",
        (product_id, start, end)
    )
    count = cur.fetchone()[0]
    conn.close()
    return count > 0


def calculate_price_with_discount(product_id, price, date):
    """
    Рассчитывает цену со скидкой 25%.

    :param product_id: id товара
    :param price: базовая цена
    :param date: дата расчёта
    :return: цена со скидкой или без
    """
    if has_orders_in_previous_month(product_id, date):
        return price
    return price * 0.75


# --- Проверка при запуске файла напрямую ---
if __name__ == "__main__":
    test_date = datetime(2026, 10, 15)

    # Проверка функции расчёта периода
    print("Период предыдущего месяца:", get_previous_month_range(test_date))
    # Ожидаем: ('2026-09-01', '2026-09-30')

    # Проверка перехода через год
    print("Переход через год:", get_previous_month_range(datetime(2026, 1, 10)))
    # Ожидаем: ('2025-12-01', '2025-12-31')