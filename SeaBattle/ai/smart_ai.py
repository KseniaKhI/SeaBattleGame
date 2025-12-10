"""
Модуль с умным искусственным интеллектом
"""

import random
from models.cell import Cell


class SmartAI:
    """Умный ИИ для компьютера"""

    def __init__(self, board):
        """
        Инициализация ИИ

        Args:
            board (Board): Игровое поле игрока
        """
        self.board = board
        self.shots = set()
        self.last_hit = None
        self.hit_direction = None
        self.hits_to_follow = []
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.mode = "hunt"

    def get_next_shot(self):
        """Получить координаты следующего выстрела"""
        if self.mode == "target" and self.hits_to_follow:
            return self.hits_to_follow.pop(0)

        if self.mode == "target" and self.last_hit:
            next_target = self.find_next_target()
            if next_target:
                return next_target

        return self.hunt_mode_shot()

    def find_next_target(self):
        """Найти следующую цель вокруг последнего попадания"""
        if not self.last_hit:
            return None

        x, y = self.last_hit

        if self.hit_direction:
            dx, dy = self.hit_direction
            nx, ny = x + dx, y + dy

            if self.is_valid_shot(nx, ny):
                return (nx, ny)
            else:
                dx, dy = -dx, -dy
                nx, ny = x + dx, y + dy
                if self.is_valid_shot(nx, ny):
                    self.hit_direction = (dx, dy)
                    return (nx, ny)

        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_shot(nx, ny):
                if self.check_line_for_hits(x, y, dx, dy):
                    self.hit_direction = (dx, dy)
                    return (nx, ny)

        self.mode = "hunt"
        self.last_hit = None
        self.hit_direction = None
        return None

    def check_line_for_hits(self, x, y, dx, dy):
        """Проверить линию на наличие попаданий"""
        hits_in_line = 0

        nx, ny = x + dx, y + dy
        while 0 <= nx < 10 and 0 <= ny < 10:
            if (nx, ny) in self.shots and self.board.grid[ny][nx] in [Cell.HIT, Cell.DESTROYED]:
                hits_in_line += 1
            nx += dx
            ny += dy

        nx, ny = x - dx, y - dy
        while 0 <= nx < 10 and 0 <= ny < 10:
            if (nx, ny) in self.shots and self.board.grid[ny][nx] in [Cell.HIT, Cell.DESTROYED]:
                hits_in_line += 1
            nx -= dx
            ny -= dy

        return hits_in_line > 0

    def hunt_mode_shot(self):
        """Стратегическая стрельба в режиме охоты"""
        priority_cells = []

        for y in range(10):
            for x in range(10):
                if self.is_valid_shot(x, y):
                    priority = self.calculate_priority(x, y)
                    priority_cells.append((priority, (x, y)))

        priority_cells.sort(reverse=True, key=lambda x: x[0])

        if priority_cells:
            return priority_cells[0][1]

        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if (x, y) not in self.shots:
                return (x, y)

    def calculate_priority(self, x, y):
        """Рассчитать приоритет клетки для выстрела"""
        priority = 0

        if (x + y) % 2 == 0:
            priority += 10

        distance_from_center = abs(x - 4.5) + abs(y - 4.5)
        priority += max(0, 9 - distance_from_center)

        if x == 0 or x == 9 or y == 0 or y == 9:
            priority -= 5

        misses_around = 0
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10:
                if (nx, ny) in self.shots and self.board.grid[ny][nx] == Cell.MISS:
                    misses_around += 1

        priority -= misses_around * 3

        hits_around = 0
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10:
                if (nx, ny) in self.shots and self.board.grid[ny][nx] in [Cell.HIT, Cell.DESTROYED]:
                    hits_around += 1

        priority += hits_around * 15

        return priority

    def is_valid_shot(self, x, y):
        """Проверить, можно ли стрелять в клетку"""
        return (0 <= x < 10 and 0 <= y < 10 and
                (x, y) not in self.shots)

    def register_shot(self, x, y, result):
        """Зарегистрировать результат выстрела"""
        self.shots.add((x, y))

        if result in ["hit", "destroyed"]:
            self.mode = "target"
            self.last_hit = (x, y)

            if result == "hit" and not self.hit_direction:
                self.build_target_chain(x, y)

            if result == "destroyed":
                self.mode = "hunt"
                self.last_hit = None
                self.hit_direction = None
                self.hits_to_follow = []
                self.mark_around_destroyed(x, y)
        else:
            if self.mode == "target" and self.hits_to_follow:
                if (x, y) in self.hits_to_follow:
                    self.hits_to_follow.remove((x, y))

            if self.mode == "target" and self.last_hit and self.hit_direction:
                self.hit_direction = None
                self.build_target_chain(self.last_hit[0], self.last_hit[1])

    def build_target_chain(self, x, y):
        """Построить цепочку целей вокруг попадания"""
        self.hits_to_follow = []

        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_shot(nx, ny):
                self.hits_to_follow.append((nx, ny))

        random.shuffle(self.hits_to_follow)

    def mark_around_destroyed(self, x, y):
        """Пометить клетки вокруг уничтоженного корабля"""
        destroyed_ship = None
        for ship in self.board.ships:
            if ship.is_destroyed() and (x, y) in ship.cells:
                destroyed_ship = ship
                break

        if not destroyed_ship:
            return

        for sx, sy in destroyed_ship.cells:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = sx + dx, sy + dy
                    if 0 <= nx < 10 and 0 <= ny < 10:
                        if (nx, ny) not in self.shots:
                            self.shots.add((nx, ny))