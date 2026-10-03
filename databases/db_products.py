"""Загрузка товаров из БД с расширенным выводом."""
import sqlite3
from config import DB_PATH


# ---------- Получение данных ----------

def get_all_products():
    """Возвращает список всех товаров."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Товар ORDER BY id")
        return cur.fetchall()


def get_products_by_category(category):
    """Товары по модели (категории)."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM Товар WHERE модель = ? ORDER BY id",
            (category,)
        )
        return cur.fetchall()


def get_products_low_stock(limit=3):
    """Товары с количеством ≤ limit (по умолчанию 3)."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM Товар WHERE количество <= ? ORDER BY количество",
            (limit,)
        )
        return cur.fetchall()


def get_categories():
    """Список всех моделей (категорий)."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT модель FROM Товар ORDER BY модель")
        return [row[0] for row in cur.fetchall()]


# ---------- Вывод ----------

def print_catalog(products, title="КАТАЛОГ"):
    """Каталог с индикатором остатка."""
    print(f"\n{'=' * 60}")
    print(f"{title} ({len(products)} товаров)")
    print("=" * 60)

    for p in products:
        # Порядок столбцов в таблице Товар:
        # 0 id | 1 брешь | 2 модель | 3 озу | 4 цена | 5 количество | 6 изображение
        product_id, name, model, ram, price, qty, _image = p

        if qty <= 3:
            highlight = "⚠️ "
        elif qty <= 5:
            highlight = "•  "
        else:
            highlight = "   "

        if qty > 5:
            indicator = "много"
        elif qty > 3:
            indicator = "мало"
        else:
            indicator = "критично"

        print(f"{highlight}{name} ({model})")
        print(f"     Цена: {price} руб. | Кол-во: {qty} ({indicator})")

    print("=" * 60)


# ---------- Демонстрация ----------

if __name__ == "__main__":
    print("1. Все товары")
    print_catalog(get_all_products(), title="ВСЕ ТОВАРЫ")

    print("\n2. Модели:")
    for cat in get_categories():
        print(f"   - {cat}")

    print("\n3. Товары с низким остатком (≤3):")
    print_catalog(get_products_low_stock(), title="НИЗКИЙ ОСТАТОК")

    models = get_categories()
    if models:
        first = models[0]
        print(f"\n4. Товары модели «{first}»:")
        print_catalog(get_products_by_category(first), title=f"МОДЕЛЬ: {first}")