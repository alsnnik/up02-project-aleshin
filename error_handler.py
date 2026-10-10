"""Обработчик ошибок приложения."""
from tkinter import messagebox


def safe_call(func, *args, **kwargs):
    """
    Безопасный вызов функции с обработкой ошибок.
    """
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as e:
        messagebox.showerror("Файл не найден", f"Не удалось открыть файл:\n{e}")
    except ConnectionError as e:
        messagebox.showerror("Ошибка подключения", f"Нет соединения:\n{e}")
    except ValueError as e:
        messagebox.showwarning("Неверное значение", f"Проверьте ввод:\n{e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Что-то пошло не так:\n{e}")
    return None


def validate_positive_int(value, field_name="Значение"):
    """
    Проверяет, что значение — положительное целое число.
    """
    try:
        number = int(value)
        if number <= 0:
            return False, f"{field_name} должно быть больше нуля"
        return True, number
    except (ValueError, TypeError):
        return False, f"{field_name} должно быть целым числом"