"""Проверка вывода полей и крайних случаев."""
import database as db


# Индексы полей (вариант «Смартфоны»)
IDX_ID = 0
IDX_BRAND = 1
IDX_MODEL = 2
IDX_RAM = 3
IDX_PRICE = 4
IDX_QTY = 5
IDX_IMAGE = 6


def test_fields():
    """Проверяет, что все поля на месте."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")

    required_count = 6
    errors = 0
    for p in products:
        if len(p) < required_count:
            print(f"❌ Товар id={p[0]}: мало полей ({len(p)})")
            errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")


def test_prices():
    """Проверяет, что у всех товаров есть цена (не None)."""
    products = db.get_all_products()
    errors = 0
    for p in products:
        if p[IDX_PRICE] is None:
            print(f"❌ Товар id={p[IDX_ID]}: нет цены")
            errors += 1
    if errors == 0:
        print("✅ У всех товаров есть цена")
    else:
        print(f"❌ Найдено товаров без цены: {errors}")


def test_quantities():
    """Проверяет, что количество у всех товаров >= 0."""
    products = db.get_all_products()
    errors = 0
    for p in products:
        if p[IDX_QTY] is None or p[IDX_QTY] < 0:
            print(f"❌ Товар id={p[IDX_ID]}: количество = {p[IDX_QTY]}")
            errors += 1
    if errors == 0:
        print("✅ У всех товаров количество >= 0")
    else:
        print(f"❌ Найдено товаров с отрицательным количеством: {errors}")


def test_has_image():
    """Проверяет, что хотя бы у одного товара есть изображение."""
    products = db.get_all_products()
    for p in products:
        if p[IDX_IMAGE]:   # путь к картинке не пустой
            print(f"✅ Найдено изображение у товара id={p[IDX_ID]}")
            return
    print("❌ Ни у одного товара нет изображения")


if __name__ == "__main__":
    print("--- test_fields ---")
    test_fields()
    print("\n--- test_prices ---")
    test_prices()
    print("\n--- test_quantities ---")
    test_quantities()
    print("\n--- test_has_image ---")
    test_has_image()