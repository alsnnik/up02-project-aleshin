"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def add_order_to_db(client, product_id, quantity):
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
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE Товар SET количество = ? WHERE id = ?",
                    (new_quantity, product_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка обновления количества: {e}")
    finally:
        conn.close()


def decrease_product_quantity(product_id, quantity):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
        row = cur.fetchone()
        if not row:
            return False
        if row[0] < quantity:
            return False
        cur.execute(
            "UPDATE Товар SET количество = количество - ? WHERE id = ?",
            (quantity, product_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка уменьшения количества: {e}")
        return False
    finally:
        conn.close()


def create_order(client, items):
    conn = get_connection()
    cur = conn.cursor()
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute("INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
                    (date, client))
        order_id = cur.lastrowid
        for product_id, size, quantity, price in items:
            cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
            row = cur.fetchone()
            if not row or row[0] < quantity:
                raise ValueError(f"Недостаточно товара id={product_id}")
            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, размер, количество, цена) "
                "VALUES (?, ?, ?, ?, ?)",
                (order_id, product_id, size, quantity, price)
            )
            cur.execute(
                "UPDATE Товар SET количество = количество - ? WHERE id = ?",
                (quantity, product_id)
            )
        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return None
    finally:
        conn.close()


def get_last_order_id():
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
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def get_all_orders():
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
