"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount, get_previous_month_range


def run_tests():
    """Прогон тестов."""
    print("=" * 70)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 70)

    # Исходные 5 тестов 
    date1 = datetime(2026, 10, 15)
    base_cases = [
        (1, 8500,  8500,  date1, "Кроссовки — есть заказы в сентябре"),
        (2, 15000, 11250, date1, "Ботинки — нет заказов → 25%"),
        (3, 12000, 12000, date1, "Туфли — есть заказы"),
        (4, 4500,  3375,  date1, "Сандалии — нет заказов → скидка"),
        (5, 6000,  4500,  date1, "Кеды — нет заказов → скидка"),
    ]

    # НОВЫЕ 5 тестов 
    extra_cases = [
        # 1. Другая дата расчёта — ноябрь 2026, значит период = октябрь 2026
        #    В октябре заказов ни у кого нет → всем скидка
        (1, 8500,  6375,  datetime(2026, 11, 10),
         "Nike в ноябре → в октябре заказов нет → скидка"),

        # 2. Дата расчёта — сентябрь 2026, период = август 2026
        #    В августе заказов нет → всем скидка
        (3, 12000, 9000,  datetime(2026, 9, 5),
         "Clarks в сентябре → в августе заказов нет → скидка"),

        # 3. Переход через год: дата 15.01.2027, период = декабрь 2026
        (2, 15000, 11250, datetime(2027, 1, 15),
         "Timberland — в декабре 2026 заказов нет → скидка"),

        # 4. Товар, которого нет в БД вообще → заказов нет → скидка
        (99, 2000, 1500,  datetime(2026, 10, 15),
         "Несуществующий товар → скидка"),

        # 5. Граничный случай: заказ ровно 01.09 должен попасть в период
        (1, 8500,  8500,  datetime(2026, 10, 1),
         "Nike 01.10 → период сентябрь → заказ 15.09 найден → без скидки"),
    ]

    # Тест функции периода 
    print("\n[Проверка функции get_previous_month_range]")
    period_cases = [
        (datetime(2026, 10, 15), ("2026-09-01", "2026-09-30")),
        (datetime(2026, 1, 10),  ("2025-12-01", "2025-12-31")),
        (datetime(2026, 3, 1),   ("2026-02-01", "2026-02-28")),
    ]
    period_passed = 0
    for date, expected in period_cases:
        result = get_previous_month_range(date)
        ok = result == expected
        mark = "✅" if ok else "❌"
        if ok:
            period_passed += 1
        print(f"{mark} {date.date()} → {result} (ожидалось {expected})")

    #  Основные тесты 
    print("\n[Базовые 5 тестов]")
    passed_base = run_block(base_cases)

    print("\n[Дополнительные 5 тестов]")
    passed_extra = run_block(extra_cases)

    # === Итог ===
    total = len(base_cases) + len(extra_cases) + len(period_cases)
    passed = passed_base + passed_extra + period_passed
    print("\n" + "=" * 70)
    print(f"ИТОГО: {passed} / {total}")
    print("=" * 70)
    return passed == total


def run_block(cases):
    """Прогон блока тестов. Возвращает число пройденных."""
    passed = 0
    for product_id, price, expected, date, comment in cases:
        result = calculate_price_with_discount(product_id, price, date)
        ok = result == expected
        mark = "✅" if ok else "❌"
        if ok:
            passed += 1
        print(f"{mark} id={product_id} [{date.date()}]: "
              f"{price} → {result} (ожидалось {expected}) — {comment}")
    return passed


if __name__ == "__main__":
    run_tests()