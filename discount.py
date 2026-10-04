"""Модуль расчёта скидки.

Вариант 13: скидка 25% на товары, по которым отсутствуют заказы
в предыдущем календарном месяце (относительно даты расчёта).
"""
from datetime import datetime, timedelta
import sqlite3
from databases.config import DB_PATH


# Параметры алгоритма (легко менять под свой вариант) 
DISCOUNT_RATE = 0.10   # для 10%
DISCOUNT_RATE = 0.15   # для 15%
DISCOUNT_RATE = 0.25   # для 25%


def get_previous_month_range(date):
    """
    Возвращает (начало, конец) предыдущего календарного месяца.

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
    Есть ли у товара заказы в предыдущем календарном месяце?

    :param product_id: id товара
    :param date: дата расчёта
    :return: True / False
    """
    start, end = get_previous_month_range(date)

    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM Заказ "
            "WHERE товар_id = ? AND дата BETWEEN ? AND ?",
            (product_id, start, end)
        )
        count = cur.fetchone()[0]
    finally:
        conn.close()

    return count > 0


def calculate_price_with_discount(product_id, price, date=None):
    """
    Рассчитывает цену товара со скидкой.

    Логика: если у товара НЕТ заказов в предыдущем календарном месяце,
    применяется скидка DISCOUNT_RATE. Иначе — цена без изменений.

    :param product_id: id товара
    :param price: базовая цена
    :param date: дата расчёта (если None — текущая дата)
    :return: цена со скидкой (float) или без (тот же тип, что price)
    """
    if date is None:
        date = datetime.now()

    if has_orders_in_previous_month(product_id, date):
        return price
    return price * (1 - DISCOUNT_RATE)


# Проверка при запуске файла напрямую 
if __name__ == "__main__":
    test_date = datetime(2026, 10, 15)

    print("Период предыдущего месяца:", get_previous_month_range(test_date))
    # Ожидаем: ('2026-09-01', '2026-09-30')

    print("Переход через год:", get_previous_month_range(datetime(2026, 1, 10)))
    # Ожидаем: ('2025-12-01', '2025-12-31')

    print("\nПроверка скидки:")
    for pid, price in [(1, 8500), (2, 15000), (3, 12000), (4, 4500), (5, 6000)]:
        result = calculate_price_with_discount(pid, price, test_date)
        print(f"  Товар {pid}: {price} → {result}")