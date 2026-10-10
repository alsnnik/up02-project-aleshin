"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


def add_order_to_db(client, product_id, quantity):
    """Добавляет новый заказ в БД."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, товар_id, количество) VALUES (?, ?, ?)",
            (date, product_id, quantity)
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка добавления заказа: {e}")
        return None
    finally:
        conn.close()


def update_product_quantity(product_id, new_quantity):
    """Обновляет количество товара в БД."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE Товар SET количество = ? WHERE id = ?",
            (new_quantity, product_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка обновления количества: {e}")
    finally:
        conn.close()


def get_last_order_id():
    """Возвращает id последнего заказа."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT MAX(id) FROM Заказ")
        row = cur.fetchone()
        return row[0] if row and row[0] is not None else None
    except sqlite3.Error as e:
        print(f"Ошибка получения id заказа: {e}")
        return None
    finally:
        conn.close()


def get_product_quantity(product_id):
    """Возвращает количество товара по id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

def get_all_orders():
    """Возвращает список всех заказов с названием товара."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Заказ.id, Заказ.дата, Товар.наименование,
               Заказ.количество
        FROM Заказ
        JOIN Товар ON Товар.id = Заказ.товар_id
        ORDER BY Заказ.id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def create_order(client):
    """Создаёт пустой заказ, возвращает его id."""
    conn = get_connection()
    cur = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    cur.execute("INSERT INTO Заказ (дата, клиент) VALUES (?, ?)", (date, client))
    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id


def add_order_item(order_id, product_id, quantity):
    """Добавляет позицию в заказ."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ПозицияЗаказа (заказ_id, товар_id, количество) VALUES (?, ?, ?)",
        (order_id, product_id, quantity)
    )
    conn.commit()
    conn.close()


def get_order_items(order_id):
    """Возвращает позиции заказа с названиями товаров."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Товар.наименование, ПозицияЗаказа.количество, Товар.цена
        FROM ПозицияЗаказа
        JOIN Товар ON Товар.id = ПозицияЗаказа.товар_id
        WHERE ПозицияЗаказа.заказ_id = ?
    """, (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows