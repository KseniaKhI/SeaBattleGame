"""
Модуль для управления отрисовкой на холстах
"""

import tkinter as tk
from models.cell import Cell


class CanvasManager:
    """Класс для управления отрисовкой на холстах"""

    def __init__(self, game_ui):
        """
        Инициализация менеджера холстов

        Args:
            game_ui (SeaBattleGame): Основной класс UI игры
        """
        self.ui = game_ui

    def draw_board(self, canvas, board, hide_ships=True):
        """Отрисовка игрового поля на холсте"""
        canvas.delete("all")

        # Размер клетки
        cell_size = 32
        offset_x = 40
        offset_y = 40

        # Номера столбцов
        for x in range(10):
            x_center = offset_x + x * cell_size + cell_size // 2
            canvas.create_text(x_center, offset_y // 2,
                               text=str(x),
                               font=("Arial", 12, "bold"),
                               fill="black")

        # Номера строк
        for y in range(10):
            y_center = offset_y + y * cell_size + cell_size // 2
            canvas.create_text(offset_x // 2, y_center,
                               text=str(y),
                               font=("Arial", 12, "bold"),
                               fill="black")

        # Сетка и клетки
        for y in range(10):
            for x in range(10):
                x1 = offset_x + x * cell_size
                y1 = offset_y + y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                cell_state = board.grid[y][x]

                # Цвет и символ
                if cell_state == Cell.EMPTY:
                    fill_color = "white"
                    symbol = ""
                elif cell_state == Cell.SHIP:
                    if hide_ships:
                        fill_color = "white"
                        symbol = ""
                    else:
                        fill_color = "#3498DB"
                        symbol = "■"
                elif cell_state == Cell.MISS:
                    fill_color = "#BDC3C7"
                    symbol = "○"
                elif cell_state == Cell.HIT:
                    fill_color = "#E74C3C"
                    symbol = "✕"
                elif cell_state == Cell.DESTROYED:
                    fill_color = "#2C3E50"
                    symbol = "☠"

                # Рисуем клетку
                canvas.create_rectangle(x1, y1, x2, y2,
                                        fill=fill_color,
                                        outline="black",
                                        width=1)

                # Символ
                if symbol:
                    font_size = 16
                    if symbol == "☠":
                        font_size = 18

                    canvas.create_text(x1 + cell_size // 2, y1 + cell_size // 2,
                                       text=symbol,
                                       font=("Arial", font_size),
                                       fill="white" if cell_state in [Cell.SHIP, Cell.DESTROYED] else "black")

        # Внешняя рамка
        canvas.create_rectangle(offset_x, offset_y,
                                offset_x + 10 * cell_size, offset_y + 10 * cell_size,
                                outline="black", width=2)