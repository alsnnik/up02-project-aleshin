"""Проверка функции print_test_report."""
from test_discount import print_test_report


# Случай 1: все тесты пройдены
print("--- Случай 1: всё хорошо ---")
print_test_report(10, 10)

print()

# Случай 2: есть ошибки
print("--- Случай 2: есть ошибки ---")
print_test_report(7, 10)