"""Стили приложения: цвета и шрифты."""
import tkinter.font as tkfont

# Цвета
COLOR_MAIN_BG = "#F5F5F5"
COLOR_SECONDARY_BG = "#E0E0E0"
COLOR_ACCENT = "#4CAF50"
COLOR_HIGHLIGHT = "#FFCDD2"

# Размеры шрифтов
FONT_SIZE_NORMAL = 11
FONT_SIZE_HEADER = 13
FONT_SIZE_TITLE = 18


def font(size=FONT_SIZE_NORMAL, bold=False):
    """Возвращает шрифт заданного размера."""
    family = "Arial"
    weight = "bold" if bold else "normal"
    return (family, size, weight)
