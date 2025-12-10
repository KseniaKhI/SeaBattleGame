"""
Модуль с классом игрового поля
"""

import random
from models.ship import Ship
from models.cell import Cell


class Board:
    """Класс для представления игрового поля"""

    def __init__(self, size=10):
        """
        Инициализация игрового поля

        Args:
            size (int): Размер поля (по умолчанию 10x10)
        """
        self.size = size
        self.grid = [[Cell.EMPTY for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.shots = set()

    def can_place_ship(self, ship, ignore_ships=False):
        """
        Проверка возможности размещения корабля

        Args:
            ship (Ship): Корабль для размещения
            ignore_ships (bool): Игнорировать проверку на пересечение с другими кораблями

        Returns:
            bool: Можно ли разместить корабль
        """
        for x, y in ship.cells:
            if not (0 <= x < self.size and 0 <= y < self.size):
                return False

            # Проверка соседних клеток
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        if not ignore_ships and self.grid[ny][nx] == Cell.SHIP:
                            return False
        return True

    def place_ship(self, ship, ignore_ships=False):
        """
        Размещение корабля на поле

        Args:
            ship (Ship): Корабль для размещения
            ignore_ships (bool): Игнорировать проверку на пересечение с другими кораблями

        Returns:
            bool: Успешно ли размещен корабль
        """
        if self.can_place_ship(ship, ignore_ships):
            for x, y in ship.cells:
                self.grid[y][x] = Cell.SHIP
            if not ignore_ships:
                self.ships.append(ship)
            return True
        return False

    def remove_ship(self, ship):
        """Удаление корабля с поля"""
        for x, y in ship.cells:
            self.grid[y][x] = Cell.EMPTY
        if ship in self.ships:
            self.ships.remove(ship)

    def auto_place_ships(self):
        """
        Автоматическая расстановка кораблей

        Returns:
            bool: Успешно ли расставлены все корабли
        """
        ships_config = [(4, 1), (3, 2), (2, 3), (1, 4)]

        for size, count in ships_config:
            for _ in range(count):
                placed = False
                attempts = 0

                while not placed and attempts < 500:
                    x = random.randint(0, self.size - 1)
                    y = random.randint(0, self.size - 1)
                    horizontal = random.choice([True, False])

                    if horizontal and x + size > self.size:
                        continue
                    if not horizontal and y + size > self.size:
                        continue

                    ship = Ship(size, x, y, horizontal)
                    placed = self.place_ship(ship)
                    attempts += 1

                if not placed:
                    return False
        return True

    def shoot(self, x, y):
        """
        Выстрел по клетке

        Args:
            x (int): Координата X
            y (int): Координата Y

        Returns:
            str: Результат выстрела ("hit", "miss", "destroyed", "already_shot")
        """
        if (x, y) in self.shots:
            return "already_shot"

        self.shots.add((x, y))

        if self.grid[y][x] == Cell.SHIP:
            self.grid[y][x] = Cell.HIT

            for ship in self.ships:
                if (x, y) in ship.cells:
                    ship.health -= 1
                    if ship.is_destroyed():
                        for sx, sy in ship.cells:
                            self.grid[sy][sx] = Cell.DESTROYED
                        return "destroyed"
                    return "hit"
            return "hit"
        else:
            self.grid[y][x] = Cell.MISS
            return "miss"

    def get_ship_at(self, x, y):
        """
        Получение корабля по координатам

        Args:
            x (int): Координата X
            y (int): Координата Y

        Returns:
            Ship or None: Корабль в указанной клетке или None
        """
        for ship in self.ships:
            if (x, y) in ship.cells:
                return ship
        return None