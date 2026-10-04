"""Создание тестовой базы данных db_variant_13.db."""
import sqlite3
import os
from config import DB_PATH


def create_database():
    """Пересоздаёт БД с эталонными данными."""
    # Удаляем старую БД
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print(f"🗑  Старая БД удалена: {DB_PATH}")
        except PermissionError:
            print("⚠️  Файл занят — очищаю таблицы внутри существующей БД")
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DROP TABLE IF EXISTS Заказ")
            cur.execute("DROP TABLE IF EXISTS Пользователь")
            cur.execute("DROP TABLE IF EXISTS Товар")
            conn.commit()
            conn.close()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Таблица Пользователь
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Пользователь (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            имя   TEXT NOT NULL
        )
    """)

    # Таблица Заказ
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Заказ (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            товар_id   INTEGER NOT NULL,
            дата       TEXT    NOT NULL,
            количество INTEGER NOT NULL
        )
    """)

    # Тестовые заказы (сентябрь 2026)
    # Товар 1 (Nike)       — ЕСТЬ заказ  → без скидки
    # Товар 2 (Timberland) — НЕТ заказов → скидка 25%
    # Товар 3 (Clarks)     — ЕСТЬ заказ  → без скидки
    # Товар 4 (Adidas)     — НЕТ заказов → скидка 25%
    # Товар 5 (Кеды)       — НЕТ заказов → скидка 25%
    orders = [
        (1, "2026-09-15", 2),
        (3, "2026-09-25", 1),
    ]
    cur.executemany(
        "INSERT INTO Заказ (товар_id, дата, количество) VALUES (?, ?, ?)",
        orders
    )

    conn.commit()
    conn.close()
    print(f"✅ БД создана: {DB_PATH}")
    print(f"   Добавлено заказов: {len(orders)}")


if __name__ == "__main__":
    create_database()