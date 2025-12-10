"""
Основной модуль пользовательского интерфейса игры
"""

import tkinter as tk
from tkinter import messagebox

from models.board import Board
from models.ship import Ship
from ai.smart_ai import SmartAI
from ui.menu_screens import MenuScreens
from ui.canvas_manager import CanvasManager


class SeaBattleGame:
    """Основной класс игры Морской бой"""

    def __init__(self):
        """Инициализация игры"""
        self.root = tk.Tk()
        self.root.title("Морской бой")

        # Полноэкранный режим
        self.root.attributes('-fullscreen', True)

        # Получаем размеры экрана
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Фиксированные размеры
        self.font_sizes = {
            'title': 36,
            'button': 16,
            'label': 14,
            'small': 12,
            'canvas': 400
        }

        # Инициализация менеджеров
        self.menu_screens = MenuScreens(self)
        self.canvas_manager = CanvasManager(self)

        # Инициализация игры
        self.init_game_state()

        # Показываем главное меню
        self.menu_screens.show_main_menu()

        # Привязка клавиш
        self.root.bind('<Escape>', self.exit_fullscreen)

    def init_game_state(self):
        """Инициализация состояния игры"""
        self.placement_mode = True
        self.player_turn = True
        self.game_over = False
        self.computer_shots = []
        self.computer_ai = None

        # Игровые доски
        self.player_board = Board()
        self.computer_board = Board()

        # Переменные для расстановки
        self.current_ship_size = None
        self.current_ship_horizontal = True
        self.ships_to_place = None
        self.start_game_btn = None
        self.status_label = None

        # Холсты
        self.player_canvas = None
        self.player_canvas_battle = None
        self.computer_canvas = None

        # Элементы интерфейса
        self.battle_title = None
        self.battle_status = None

    def exit_fullscreen(self, event=None):
        """Выход из полноэкранного режима"""
        self.root.attributes('-fullscreen', False)
        self.root.geometry(f"{self.screen_width - 100}x{self.screen_height - 100}")

    # Методы меню
    def show_main_menu(self):
        """Показывает главное меню"""
        self.menu_screens.show_main_menu()

    def start_game_setup(self):
        """Начинает расстановку кораблей"""
        self.init_game_state()
        self.menu_screens.show_placement_menu()

        # Привязка событий
        self.player_canvas.bind("<Motion>", self.on_player_hover)
        self.player_canvas.bind("<Button-1>", self.on_player_click)
        self.player_canvas.bind("<Button-3>", self.on_player_right_click)

        # Отрисовка пустого поля
        self.canvas_manager.draw_board(self.player_canvas, self.player_board, hide_ships=False)

    # Методы управления игрой
    def update_ship_buttons(self):
        """Обновляет состояние кнопок кораблей"""
        for ship_info in self.ships_to_place:
            if ship_info["placed"] >= ship_info["count"]:
                ship_info["button"].config(state=tk.DISABLED, bg="#95A5A6")
            else:
                ship_info["button"].config(state=tk.NORMAL, bg="#3498DB")

    def select_ship(self, size):
        """Выбор корабля для размещения"""
        for ship_info in self.ships_to_place:
            if ship_info["size"] == size:
                if ship_info["placed"] >= ship_info["count"]:
                    self.status_label.config(text=f"Все {size}-палубные корабли уже размещены!")
                    return
                break

        self.current_ship_size = size
        self.current_ship_horizontal = True
        orient = "горизонтально" if self.current_ship_horizontal else "вертикально"
        self.status_label.config(text=f"Выбран {size}-палубный корабль ({orient})")

    def rotate_ship(self):
        """Поворот корабля"""
        if self.current_ship_size:
            self.current_ship_horizontal = not self.current_ship_horizontal
            orient = "горизонтально" if self.current_ship_horizontal else "вертикально"
            self.status_label.config(text=f"Корабль повёрнут: {orient}")

    def on_player_hover(self, event):
        """Предпросмотр размещения корабля"""
        if not self.current_ship_size or not self.placement_mode:
            return

        cell_size = 32
        offset_x = 40
        offset_y = 40

        x = (event.x - offset_x) // cell_size
        y = (event.y - offset_y) // cell_size

        if 0 <= x < 10 and 0 <= y < 10:
            if self.current_ship_horizontal and x + self.current_ship_size > 10:
                x = 10 - self.current_ship_size
            elif not self.current_ship_horizontal and y + self.current_ship_size > 10:
                y = 10 - self.current_ship_size

            if x >= 0 and y >= 0:
                temp_board = Board()
                temp_board.grid = [row[:] for row in self.player_board.grid]
                temp_ship = Ship(self.current_ship_size, x, y, self.current_ship_horizontal)

                can_place = temp_board.can_place_ship(temp_ship)

                if can_place:
                    count_placed = 0
                    for placed_ship in self.player_board.ships:
                        if placed_ship.size == self.current_ship_size:
                            count_placed += 1

                    for ship_info in self.ships_to_place:
                        if ship_info["size"] == self.current_ship_size:
                            if count_placed >= ship_info["count"]:
                                can_place = False
                            break

                if can_place:
                    temp_board.place_ship(temp_ship, ignore_ships=True)

                self.canvas_manager.draw_board(self.player_canvas, temp_board, hide_ships=False)

    def on_player_click(self, event):
        """Размещение корабля"""
        if not self.current_ship_size or not self.placement_mode:
            return

        cell_size = 32
        offset_x = 40
        offset_y = 40

        x = (event.x - offset_x) // cell_size
        y = (event.y - offset_y) // cell_size

        if 0 <= x < 10 and 0 <= y < 10:
            if self.current_ship_horizontal and x + self.current_ship_size > 10:
                x = 10 - self.current_ship_size
            elif not self.current_ship_horizontal and y + self.current_ship_size > 10:
                y = 10 - self.current_ship_size

            if x >= 0 and y >= 0:
                ship = Ship(self.current_ship_size, x, y, self.current_ship_horizontal)

                if self.player_board.can_place_ship(ship):
                    count_placed = 0
                    for placed_ship in self.player_board.ships:
                        if placed_ship.size == self.current_ship_size:
                            count_placed += 1

                    for ship_info in self.ships_to_place:
                        if ship_info["size"] == self.current_ship_size:
                            if count_placed >= ship_info["count"]:
                                self.status_label.config(text=f"Максимум {ship_info['count']} шт. таких кораблей!")
                                return
                            break

                    self.player_board.place_ship(ship)

                    for ship_info in self.ships_to_place:
                        if ship_info["size"] == self.current_ship_size:
                            ship_info["placed"] += 1
                            break

                    self.update_ship_buttons()

                    placed_total = sum(s["placed"] for s in self.ships_to_place)

                    if placed_total < 10:
                        self.status_label.config(text=f"Корабль размещен! Размещено: {placed_total}/10")
                        self.current_ship_size = None
                    else:
                        self.status_label.config(text="Все корабли размещены! Нажмите 'НАЧАТЬ БИТВУ'")
                        self.current_ship_size = None
                        self.start_game_btn.config(state=tk.NORMAL, bg="#27AE60")

                    self.canvas_manager.draw_board(self.player_canvas, self.player_board, hide_ships=False)
                else:
                    self.status_label.config(text="Нельзя разместить корабль здесь!")

    def on_player_right_click(self, event):
        """Удаление корабля"""
        if not self.placement_mode:
            return

        cell_size = 32
        offset_x = 40
        offset_y = 40

        x = (event.x - offset_x) // cell_size
        y = (event.y - offset_y) // cell_size

        if 0 <= x < 10 and 0 <= y < 10:
            for ship in self.player_board.ships[:]:
                if (x, y) in ship.cells:
                    self.player_board.remove_ship(ship)

                    for ship_info in self.ships_to_place:
                        if ship_info["size"] == ship.size:
                            ship_info["placed"] -= 1
                            break

                    self.update_ship_buttons()

                    placed_total = sum(s["placed"] for s in self.ships_to_place)
                    self.status_label.config(text=f"Корабль удален. Размещено: {placed_total}/10")
                    self.start_game_btn.config(state=tk.DISABLED, bg="#2C3E50")

                    self.canvas_manager.draw_board(self.player_canvas, self.player_board, hide_ships=False)
                    break

    def auto_place_ships(self):
        """Автоматическая расстановка кораблей"""
        self.player_board = Board()

        for ship_info in self.ships_to_place:
            ship_info["placed"] = 0

        if self.player_board.auto_place_ships():
            for ship in self.player_board.ships:
                for ship_info in self.ships_to_place:
                    if ship_info["size"] == ship.size:
                        ship_info["placed"] += 1
                        break

            self.update_ship_buttons()
            self.canvas_manager.draw_board(self.player_canvas, self.player_board, hide_ships=False)
            self.status_label.config(text="Все корабли автоматически размещены!")
            self.start_game_btn.config(state=tk.NORMAL, bg="#27AE60")
            self.current_ship_size = None
        else:
            messagebox.showerror("Ошибка", "Не удалось разместить корабли!")

    def clear_ships(self):
        """Очистка всех кораблей"""
        self.player_board = Board()

        for ship_info in self.ships_to_place:
            ship_info["placed"] = 0

        self.update_ship_buttons()
        self.canvas_manager.draw_board(self.player_canvas, self.player_board, hide_ships=False)
        self.status_label.config(text="Поле очищено. Выберите корабли.")
        self.start_game_btn.config(state=tk.DISABLED, bg="#2C3E50")
        self.current_ship_size = None

    def start_battle(self):
        """Начало битвы"""
        placed_count = sum(s["placed"] for s in self.ships_to_place)
        if placed_count < 10:
            messagebox.showwarning("Не все корабли", "Разместите все 10 кораблей!")
            return

        if not self.computer_board.auto_place_ships():
            messagebox.showerror("Ошибка", "Не удалось расставить корабли компьютера!")
            return

        # Инициализация умного ИИ
        self.computer_ai = SmartAI(self.player_board)

        self.placement_mode = False
        self.show_battle_screen()

    def show_battle_screen(self):
        """Показывает экран битвы"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Основной фрейм с фиксированной структурой
        main_frame = tk.Frame(self.root, bg="#ECF0F1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Заголовок
        title_frame = tk.Frame(main_frame, bg="#2C3E50", height=70)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        self.battle_title = tk.Label(title_frame, text="МОРСКОЙ БОЙ - ИДЁТ БИТВА",
                                     font=("Arial", 28, "bold"),
                                     fg="#ECF0F1", bg="#2C3E50")
        self.battle_title.pack(expand=True)

        # Игровые поля
        fields_frame = tk.Frame(main_frame, bg="#ECF0F1")
        fields_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Левое поле (игрок)
        left_panel = tk.Frame(fields_frame, bg="#ECF0F1")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        player_field_frame = tk.Frame(left_panel, bg="#ECF0F1")
        player_field_frame.pack(expand=True)

        player_label = tk.Label(player_field_frame, text="ВАШЕ ПОЛЕ",
                                font=("Arial", 18, "bold"), bg="#ECF0F1")
        player_label.pack(pady=5)

        self.player_canvas_battle = tk.Canvas(player_field_frame,
                                              width=self.font_sizes['canvas'],
                                              height=self.font_sizes['canvas'],
                                              bg="white", relief=tk.RAISED, bd=2)
        self.player_canvas_battle.pack()

        # Правое поле (компьютер)
        right_panel = tk.Frame(fields_frame, bg="#ECF0F1")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        computer_field_frame = tk.Frame(right_panel, bg="#ECF0F1")
        computer_field_frame.pack(expand=True)

        computer_label = tk.Label(computer_field_frame, text="ПОЛЕ ПРОТИВНИКА",
                                  font=("Arial", 18, "bold"), bg="#ECF0F1")
        computer_label.pack(pady=5)

        self.computer_canvas = tk.Canvas(computer_field_frame,
                                         width=self.font_sizes['canvas'],
                                         height=self.font_sizes['canvas'],
                                         bg="white", relief=tk.RAISED, bd=2)
        self.computer_canvas.pack()
        self.computer_canvas.bind("<Button-1>", self.on_computer_click)

        # Статус
        status_frame = tk.Frame(main_frame, bg="#ECF0F1", height=80)
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        status_frame.pack_propagate(False)

        self.battle_status = tk.Label(status_frame,
                                      text="ВАШ ХОД. Стреляйте по полю противника!",
                                      font=("Arial", 16, "bold"),
                                      bg="#ECF0F1", fg="#2C3E50",
                                      wraplength=800,
                                      justify=tk.CENTER)
        self.battle_status.pack(expand=True)

        # Кнопка сдаться
        surrender_frame = tk.Frame(main_frame, bg="#ECF0F1", height=60)
        surrender_frame.pack(fill=tk.X, padx=20, pady=5)
        surrender_frame.pack_propagate(False)

        surrender_btn = tk.Button(surrender_frame, text="СДАТЬСЯ",
                                  command=self.surrender,
                                  font=("Arial", self.font_sizes['button'], "bold"),
                                  bg="#E74C3C", fg="white",
                                  width=20, height=2)
        surrender_btn.pack(pady=10)

        # Легенда
        legend_frame = tk.LabelFrame(main_frame, text="ЛЕГЕНДА",
                                     font=("Arial", 14, "bold"), bg="#ECF0F1")
        legend_frame.pack(fill=tk.X, padx=10, pady=5)

        legend_items = [
            ("■", "Ваш корабль", "#3498DB"),
            ("✕", "Попадание", "#E74C3C"),
            ("○", "Промах", "#BDC3C7"),
            ("☠", "Уничтожен", "#2C3E50"),
            ("□", "Пустая клетка", "#FFFFFF")
        ]

        legend_row = tk.Frame(legend_frame, bg="#ECF0F1")
        legend_row.pack(fill=tk.X, padx=10, pady=5)

        for symbol, desc, color in legend_items:
            item_frame = tk.Frame(legend_row, bg="#ECF0F1")
            item_frame.pack(side=tk.LEFT, padx=15)

            color_frame = tk.Frame(item_frame, width=30, height=30, bg=color, relief=tk.RAISED, bd=1)
            color_frame.pack(side=tk.LEFT)
            color_frame.pack_propagate(False)

            color_label = tk.Label(color_frame, text=symbol,
                                   font=("Arial", 14),
                                   bg=color, fg="white" if color in ["#3498DB", "#2C3E50", "#E74C3C"] else "black")
            color_label.pack(expand=True)

            desc_label = tk.Label(item_frame, text=desc,
                                  font=("Arial", self.font_sizes['small']),
                                  bg="#ECF0F1", anchor=tk.W)
            desc_label.pack(side=tk.LEFT, padx=5)

        # Отрисовываем поля
        self.canvas_manager.draw_board(self.player_canvas_battle, self.player_board, hide_ships=False)
        self.canvas_manager.draw_board(self.computer_canvas, self.computer_board, hide_ships=True)

    def on_computer_click(self, event):
        """Выстрел по полю компьютера"""
        if not self.player_turn or self.game_over:
            return

        cell_size = 32
        offset_x = 40
        offset_y = 40

        x = (event.x - offset_x) // cell_size
        y = (event.y - offset_y) // cell_size

        if 0 <= x < 10 and 0 <= y < 10:
            self.player_shoot(x, y)

    def player_shoot(self, x, y):
        """Обработка выстрела игрока"""
        result = self.computer_board.shoot(x, y)

        if result == "already_shot":
            self.battle_status.config(text="Вы уже стреляли в эту клетку!")
            return

        self.canvas_manager.draw_board(self.computer_canvas, self.computer_board, hide_ships=True)

        if result == "miss":
            self.battle_status.config(text="Промах! Ход компьютера...")
            self.player_turn = False
            self.root.after(1000, self.smart_computer_turn)
        elif result == "hit":
            self.battle_status.config(text="Попадание! Стреляйте ещё!")
        elif result == "destroyed":
            self.battle_status.config(text="Корабль противника уничтожен! Стреляйте ещё!")

        if self.check_game_over():
            return

    def smart_computer_turn(self):
        """Ход умного компьютера"""
        if self.game_over:
            return

        # Получаем следующий выстрел от ИИ
        x, y = self.computer_ai.get_next_shot()

        result = self.player_board.shoot(x, y)

        # Регистрируем выстрел в ИИ
        self.computer_ai.register_shot(x, y, result)

        # Обновляем поле игрока
        self.canvas_manager.draw_board(self.player_canvas_battle, self.player_board, hide_ships=False)

        if result == "miss":
            self.battle_status.config(
                text=f"Компьютер стрелял в ({x},{y}) - Промах!\nВАШ ХОД.")
            self.player_turn = True
        else:
            hit_text = "Попадание" if result == "hit" else "Корабль уничтожен"
            self.battle_status.config(
                text=f"Компьютер стрелял в ({x},{y}) - {hit_text}!\nКомпьютер стреляет ещё...")
            self.root.after(1500, self.smart_computer_turn)

        if self.check_game_over():
            return

    def check_game_over(self):
        """Проверка окончания игры"""
        player_ships_alive = any(not ship.is_destroyed() for ship in self.player_board.ships)
        computer_ships_alive = any(not ship.is_destroyed() for ship in self.computer_board.ships)

        if not player_ships_alive or not computer_ships_alive:
            self.game_over = True
            self.computer_canvas.unbind("<Button-1>")

            self.canvas_manager.draw_board(self.computer_canvas, self.computer_board, hide_ships=False)

            winner = "КОМПЬЮТЕР" if not player_ships_alive else "ВЫ"

            self.show_game_over_screen(winner)
            return True

        return False

    def show_game_over_screen(self, winner):
        """Показывает экран окончания игры"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Игра окончена!")
        result_window.geometry("400x300")
        result_window.resizable(False, False)
        result_window.configure(bg="#2C3E50")
        result_window.transient(self.root)
        result_window.grab_set()

        result_window.update_idletasks()
        width = result_window.winfo_width()
        height = result_window.winfo_height()
        x = (self.screen_width // 2) - (width // 2)
        y = (self.screen_height // 2) - (height // 2)
        result_window.geometry(f'{width}x{height}+{x}+{y}')

        result_label = tk.Label(result_window,
                                text=f"ПОБЕДИЛ: {winner}",
                                font=("Arial", 24, "bold"),
                                fg="#ECF0F1", bg="#2C3E50")
        result_label.pack(pady=30)

        player_score = sum(1 for s in self.computer_board.ships if s.is_destroyed())
        computer_score = sum(1 for s in self.player_board.ships if s.is_destroyed())

        stats_text = f"Уничтожено кораблей:\nВы: {player_score}/10\nКомпьютер: {computer_score}/10"

        stats_label = tk.Label(result_window, text=stats_text,
                               font=("Arial", 14),
                               fg="#BDC3C7", bg="#2C3E50")
        stats_label.pack(pady=20)

        new_game_btn = tk.Button(result_window, text="НОВАЯ ИГРА",
                                 command=self.new_game,
                                 font=("Arial", 14, "bold"),
                                 bg="#3498DB", fg="white",
                                 width=15, height=2)
        new_game_btn.pack(pady=20)

    def surrender(self):
        """Сдача"""
        if messagebox.askyesno("Сдаться", "Вы уверены, что хотите сдаться?"):
            self.game_over = True
            self.computer_canvas.unbind("<Button-1>")

            self.show_surrender_screen()

    def show_surrender_screen(self):
        """Показывает экран сдачи"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Игра окончена!")
        result_window.geometry("400x250")
        result_window.resizable(False, False)
        result_window.configure(bg="#2C3E50")
        result_window.transient(self.root)
        result_window.grab_set()

        result_window.update_idletasks()
        width = result_window.winfo_width()
        height = result_window.winfo_height()
        x = (self.screen_width // 2) - (width // 2)
        y = (self.screen_height // 2) - (height // 2)
        result_window.geometry(f'{width}x{height}+{x}+{y}')

        result_label = tk.Label(result_window,
                                text="ВЫ СДАЛИСЬ\nПОБЕДИЛ: КОМПЬЮТЕР",
                                font=("Arial", 20, "bold"),
                                fg="#ECF0F1", bg="#2C3E50")
        result_label.pack(pady=30)

        new_game_btn = tk.Button(result_window, text="НОВАЯ ИГРА",
                                 command=self.new_game,
                                 font=("Arial", 14, "bold"),
                                 bg="#3498DB", fg="white",
                                 width=15, height=2)
        new_game_btn.pack(pady=30)

    def new_game(self):
        """Начинает новую игру"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

        self.init_game_state()
        self.show_main_menu()

    def run(self):
        """Запуск игры"""
        self.root.mainloop()