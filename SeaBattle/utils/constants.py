"""
Модуль с константами игры
"""

# Цвета
COLORS = {
    'background': "#2C3E50",
    'primary': "#3498DB",
    'success': "#27AE60",
    'danger': "#E74C3C",
    'warning': "#F39C12",
    'info': "#16A085",
    'light': "#ECF0F1",
    'dark': "#2C3E50",
    'gray': "#BDC3C7"
}

# Настройки игры
GAME_SETTINGS = {
    'board_size': 10,
    'ship_configs': [(4, 1), (3, 2), (2, 3), (1, 4)],
    'canvas_size': 400,
    'cell_size': 32,
    'font_sizes': {
        'title': 36,
        'button': 16,
        'label': 14,
        'small': 12
    }
}

# Легенда
LEGEND_ITEMS = [
    ("■", "Ваш корабль", "#3498DB"),
    ("✕", "Попадание", "#E74C3C"),
    ("○", "Промах", "#BDC3C7"),
    ("☠", "Уничтожен", "#2C3E50"),
    ("□", "Пустая клетка", "#FFFFFF")
]