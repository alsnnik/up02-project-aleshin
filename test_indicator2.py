"""Тестирование каталога."""
import database as db


# Индексы полей (вариант «Смартфоны»)
IDX_ID = 0
IDX_BRAND = 1
IDX_MODEL = 2
IDX_PRICE = 4
IDX_QTY = 5
IDX_IMAGE = 6


def test_db_available():
    """Проверяет, что БД доступна."""
    try:
        products = db.get_all_products()
        return isinstance(products, list)
    except Exception as e:
        print(f"❌ БД недоступна: {e}")
        return False


def test_products_count():
    """Проверяет, что товары загружены."""
    products = db.get_all_products()
    return len(products) > 0


def test_product_fields():
    """Проверяет, что у всех товаров достаточно полей (>= 7)."""
    products = db.get_all_products()
    for p in products:
        if len(p) < 7:
            print(f"❌ Товар id={p[IDX_ID]}: мало полей ({len(p)})")
            return False
    return True


def test_prices_are_numbers():
    """Проверяет, что все цены — числа."""
    products = db.get_all_products()
    for p in products:
        if not isinstance(p[IDX_PRICE], (int, float)):
            print(f"❌ Товар id={p[IDX_ID]}: цена не число")
            return False
    return True


def test_quantity_not_negative():
    """Проверяет, что количество не отрицательное."""
    products = db.get_all_products()
    for p in products:
        if p[IDX_QTY] < 0:
            print(f"❌ Товар id={p[IDX_ID]}: отрицательное количество")
            return False
    return True


def test_names_not_empty():
    """Проверяет, что у всех товаров есть название (бренд и модель)."""
    products = db.get_all_products()
    for p in products:
        if not p[IDX_BRAND] or not p[IDX_MODEL]:
            print(f"❌ Товар id={p[IDX_ID]}: пустое название")
            return False
    return True


# --- ДЗ: проверка изображения ---
def test_has_image():
    """Проверяет, что хотя бы у одного товара есть изображение."""
    products = db.get_all_products()
    for p in products:
        if p[IDX_IMAGE]:
            print(f"✅ Изображение найдено у товара id={p[IDX_ID]}")
            return True
    print("❌ Ни у одного товара нет изображения")
    return False


def run_all_tests():
    """Прогон всех тестов каталога."""
    tests = [
        ("БД доступна", test_db_available),
        ("Товары загружены", test_products_count),
        ("У всех товаров нужные поля", test_product_fields),
        ("Все цены — числа", test_prices_are_numbers),
        ("Количество не отрицательное", test_quantity_not_negative),
        ("Названия не пустые", test_names_not_empty),
        ("Хотя бы одно изображение", test_has_image),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА")
    print("=" * 60)

    passed = 0
    for name, func in tests:
        result = func()
        status = "✅" if result else "❌"
        if result:
            passed += 1
        print(f"{status} {name}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(tests)}")


if __name__ == "__main__":
    run_all_tests()