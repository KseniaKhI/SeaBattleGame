"""
Модуль с классом корабля
"""


class Ship:
    """Класс для представления корабля"""

    def __init__(self, size, x, y, horizontal):
        """
        Инициализация корабля

        Args:
            size (int): Размер корабля (количество палуб)
            x (int): Координата X начальной точки
            y (int): Координата Y начальной точки
            horizontal (bool): Ориентация (True - горизонтальная, False - вертикальная)
        """
        self.size = size
        self.x = x
        self.y = y
        self.horizontal = horizontal
        self.health = size
        self.cells = []
        self.update_cells()

    def update_cells(self):
        """Обновление списка клеток, занимаемых кораблем"""
        self.cells = []
        for i in range(self.size):
            if self.horizontal:
                self.cells.append((self.x + i, self.y))
            else:
                self.cells.append((self.x, self.y + i))

    def is_destroyed(self):
        """Проверка, уничтожен ли корабль"""
        return self.health <= 0

    def __repr__(self):
        return f"Ship(size={self.size}, pos=({self.x},{self.y}), horizontal={self.horizontal})"