"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    test_cases = [
        # (product_id, price, date, expected, comment)

        # --- Базовые 5 тестов (сентябрь = период) ---
        (1, 8500,  datetime(2026, 10, 15), 8500,  "Nike: заказ 15.09 → без скидки"),
        (2, 15000, datetime(2026, 10, 15), 11250, "Timberland: заказов нет → скидка"),
        (3, 12000, datetime(2026, 10, 15), 12000, "Clarks: заказ 25.09 → без скидки"),
        (4, 4500,  datetime(2026, 10, 15), 3375,  "Adidas: заказов нет → скидка"),
        (5, 6000,  datetime(2026, 10, 15), 4500,  "Кеды: заказов нет → скидка"),

        # --- Новые тесты: другая дата расчёта → другой период ---
        (2, 15000, datetime(2026, 11, 15), 11250, "Timberland: октябрь пустой → скидка"),
        (1, 8500,  datetime(2026, 11, 15), 6375,  "Nike: октябрь пустой → скидка"),
        (4, 4500,  datetime(2026, 9, 1),   3375,  "Adidas: август пустой → скидка"),
    ]

    print("=" * 70)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 70)

    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Товар {product_id} на {date.date()}: "
              f"{price} → {result} (ожидалось {expected}) — {comment}")

    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()