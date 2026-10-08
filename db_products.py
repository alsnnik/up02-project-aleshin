"""Загрузка товаров из БД в объекты класса Product."""
import sqlite3
from config import DB_PATH
from models import Product


# Базовые функции

def get_all_products():
    """Возвращает список объектов Product из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [Product.from_row(row) for row in rows]


def get_products_by_category(category):
    """Возвращает список объектов Product по модели (категории)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE модель = ?", (category,))
    rows = cur.fetchall()
    conn.close()
    return [Product.from_row(row) for row in rows]


def get_products_low_stock(limit=3):
    """Возвращает товары с количеством ≤ limit (по умолчанию 3)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= ? ORDER BY количество", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [Product.from_row(row) for row in rows]


def get_categories():
    """Список всех уникальных моделей (категорий)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT модель FROM Товар ORDER BY модель")
    result = [row[0] for row in cur.fetchall()]
    conn.close()
    return result


# Вывод 

def print_products(products):
    """Простой вывод товаров."""
    print(f"\nВсего товаров: {len(products)}\n")
    for p in products:
        print(p.info())
        print("-" * 60)


def print_catalog_with_highlight(products, title="КАТАЛОГ"):
    """Выводит каталог с подсветкой для товаров ≤ 3."""
    print(f"\n{'=' * 70}")
    print(f"{title} ({len(products)} товаров)")
    print("=" * 70)

    if not products:
        print("   Товары не найдены.")
    else:
        for p in products:
            # Подсветка в зависимости от остатка
            if p.quantity <= 3:
                highlight = "⚠️ "
            elif p.quantity <= 5:
                highlight = "•  "
            else:
                highlight = "   "

            print(f"{highlight}{p.info()}")

    print("=" * 70)


#  Демонстрация 

if __name__ == "__main__":
    print("1. Все товары:")
    print_catalog_with_highlight(get_all_products(), title="ВСЕ ТОВАРЫ")

    print("\n2. Доступные модели (категории):")
    for cat in get_categories():
        print(f"   - {cat}")

    print("\n3. Товары категории «Смартфон»:")
    print_catalog_with_highlight(
        get_products_by_category("Смартфон"),
        title="КАТЕГОРИЯ: Смартфон"
    )

    print("\n4. Товары с низким остатком (≤3):")
    print_catalog_with_highlight(
        get_products_low_stock(),
        title="НИЗКИЙ ОСТАТОК"
    )