"""Настройки проекта."""
import os

# Путь к базе данных. 
# Вариант 1 (проще, если запускаете из корня проекта):
DB_PATH = "databases/db_variant_13.db"

# Вариант 2 (надежнее, если запускаете из разных мест):
# DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "databases", "db_variant_13.db")

APP_TITLE = "Электроника — Каталог товаров"
FONT_FAMILY = "Arial"
COLOR_HIGHLIGHT = "#FFE4B5"