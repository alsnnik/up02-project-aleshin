"""Модуль расчёта скидки."""
from datetime import datetime, timedelta
import sqlite3
from config import DB_PATH


DISCOUNT_RATE = 0.25   # размер скидки: 25%


def get_previous_month_range(date):
    """Возвращает (начало, конец) предыдущего календарного месяца."""
    first_day = date.replace(day=1)
    last_day_prev = first_day - timedelta(days=1)
    first_day_prev = last_day_prev.replace(day=1)
    return (
        first_day_prev.strftime("%Y-%m-%d"),
        last_day_prev.strftime("%Y-%m-%d")
    )


def has_orders_in_previous_month(product_id, date):
    """Есть ли у товара заказы в предыдущем календарном месяце?"""
    start, end = get_previous_month_range(date)

    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM Заказ "
            "WHERE товар_id = ? AND date(дата) BETWEEN ? AND ?",
            (product_id, start, end)
        )
        count = cur.fetchone()[0]
    finally:
        conn.close()

    return count > 0


def calculate_price_with_discount(product_id, price, date=None):
    """Рассчитывает цену со скидкой 25%."""
    if date is None:
        date = datetime.now()

    if has_orders_in_previous_month(product_id, date):
        return price
    return price * (1 - DISCOUNT_RATE)


if __name__ == "__main__":
    test_date = datetime(2026, 10, 15)
    print("Период:", get_previous_month_range(test_date))
    print("Переход через год:", get_previous_month_range(datetime(2026, 1, 10)))