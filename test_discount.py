"""Тестирование алгоритма скидки с граничными случаями."""
from datetime import datetime
from discount import calculate_price_with_discount


def print_test_report(passed, total):
    """Выводит отчёт о тестировании (см. Задание 2)."""
    print("=" * 40)
    print("ОТЧЁТ О ТЕСТИРОВАНИИ")
    print(f"Пройдено: {passed} / {total}")
    result = "✅ УСПЕХ" if passed == total else "❌ ЕСТЬ ОШИБКИ"
    print(f"Результат: {result}")
    print("=" * 40)


def run_tests():
    test_cases = [
        # (product_id, price, date, expected, comment)

        # --- Базовые 5 тестов ---
        (1, 8500,  datetime(2026, 10, 15), 8500,  "Nike: заказ 15.09 → без скидки"),
        (2, 15000, datetime(2026, 10, 15), 11250, "Timberland: заказов нет → скидка"),
        (3, 12000, datetime(2026, 10, 15), 12000, "Clarks: заказ 25.09 → без скидки"),
        (4, 4500,  datetime(2026, 10, 15), 3375,  "Adidas: заказов нет → скидка"),
        (5, 6000,  datetime(2026, 10, 15), 4500,  "Кеды: заказов нет → скидка"),

        # --- Новые 5 тестов: граничные случаи (Задание 1) ---
        (1, 8500,  datetime(2026, 10, 1),  8500,  "1-е число месяца: период сентябрь → заказ найден"),
        (2, 15000, datetime(2026, 10, 31), 11250, "Последний день месяца: у товара 2 заказов нет → скидка"),
        (5, 0,     datetime(2026, 10, 15), 0,     "Нулевая цена: 0 × 0.75 = 0"),
        (4, 4500,  datetime(2026, 10, 15), 3375,  "Отрицательное количество: валидация не в алгоритме скидки"),
        (3, 12000, datetime(2026, 11, 1),  9000,  "Заказ был в сентябре, но в октябре нет → скидка"),
    ]

    print("=" * 75)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (С ГРАНИЧНЫМИ СЛУЧАЯМИ)")
    print("=" * 75)

    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Товар {product_id} на {date.date()}: "
              f"{price} → {result} (ожидалось {expected}) — {comment}")

    print()
    print_test_report(passed, len(test_cases))
    return passed == len(test_cases)


if __name__ == "__main__":
    run_tests()