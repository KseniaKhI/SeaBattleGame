"""
Модуль с экранами меню
"""

import tkinter as tk


class MenuScreens:
    """Класс для управления экранами меню"""

    def __init__(self, game_ui):
        """
        Инициализация экранов меню

        Args:
            game_ui (SeaBattleGame): Основной класс UI игры
        """
        self.ui = game_ui

    def show_main_menu(self):
        """Показывает главное меню"""
        for widget in self.ui.root.winfo_children():
            widget.destroy()

        # Фон
        bg_frame = tk.Frame(self.ui.root, bg="#2C3E50")
        bg_frame.pack(fill=tk.BOTH, expand=True)

        # Центральный фрейм
        center_frame = tk.Frame(bg_frame, bg="#2C3E50")
        center_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Заголовок
        title_label = tk.Label(center_frame, text="МОРСКОЙ БОЙ",
                               font=("Arial", self.ui.font_sizes['title'], "bold"),
                               fg="#ECF0F1", bg="#2C3E50")
        title_label.pack(pady=30)

        # Фрейм для кнопок
        buttons_frame = tk.Frame(center_frame, bg="#2C3E50")
        buttons_frame.pack(pady=20)

        # Кнопка начать игру
        start_button = tk.Button(buttons_frame, text="НАЧАТЬ ИГРУ",
                                 command=self.ui.start_game_setup,
                                 font=("Arial", self.ui.font_sizes['button'], "bold"),
                                 bg="#3498DB", fg="white",
                                 activebackground="#2980B9",
                                 width=18, height=2,
                                 relief=tk.RAISED, bd=3)
        start_button.pack(pady=10)

        # Кнопка выхода
        exit_button = tk.Button(buttons_frame, text="ВЫЙТИ",
                                command=self.ui.root.quit,
                                font=("Arial", self.ui.font_sizes['button'], "bold"),
                                bg="#E74C3C", fg="white",
                                activebackground="#C0392B",
                                width=18, height=2,
                                relief=tk.RAISED, bd=3)
        exit_button.pack(pady=10)

        # Правила
        rules_frame = tk.Frame(bg_frame, bg="#2C3E50")
        rules_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        rules = [
            "Правила игры:",
            "1. Расставьте 10 кораблей на своём поле",
            "2. Корабли не должны касаться друг друга",
            "3. По очереди стреляйте по полю противника",
            "4. Побеждает тот, кто первым уничтожит все корабли",
            "",
            "Управление: ESC - выйти из полноэкранного режима"
        ]

        for rule in rules:
            label = tk.Label(rules_frame, text=rule,
                             font=("Arial", self.ui.font_sizes['small']),
                             fg="#BDC3C7", bg="#2C3E50",
                             justify=tk.CENTER)
            label.pack()

    def show_placement_menu(self):
        """Показывает меню расстановки кораблей"""
        for widget in self.ui.root.winfo_children():
            widget.destroy()

        # Основной фрейм
        main_frame = tk.Frame(self.ui.root, bg="#ECF0F1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Заголовок
        title_frame = tk.Frame(main_frame, bg="#2C3E50", height=70)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="РАССТАНОВКА КОРАБЛЕЙ",
                               font=("Arial", 28, "bold"),
                               fg="#ECF0F1", bg="#2C3E50")
        title_label.pack(expand=True)

        # Основной контент (две колонки)
        content_frame = tk.Frame(main_frame, bg="#ECF0F1")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Левая колонка - поле игрока
        left_column = tk.Frame(content_frame, bg="#ECF0F1")
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Поле игрока
        field_frame = tk.Frame(left_column, bg="#ECF0F1")
        field_frame.pack(expand=True)

        field_label = tk.Label(field_frame, text="ВАШЕ ПОЛЕ",
                               font=("Arial", 18, "bold"), bg="#ECF0F1")
        field_label.pack(pady=5)

        # Холст игрока
        self.ui.player_canvas = tk.Canvas(field_frame, width=self.ui.font_sizes['canvas'],
                                          height=self.ui.font_sizes['canvas'],
                                          bg="white", relief=tk.RAISED, bd=2)
        self.ui.player_canvas.pack()

        # Правая колонка - управление
        right_column = tk.Frame(content_frame, bg="#ECF0F1", width=350)
        right_column.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        right_column.pack_propagate(False)

        # Статус
        status_frame = tk.Frame(right_column, bg="#ECF0F1", height=100)
        status_frame.pack(fill=tk.X, pady=5)
        status_frame.pack_propagate(False)

        self.ui.status_label = tk.Label(status_frame,
                                        text="Разместите свои корабли\nна поле слева\n\nВыберите корабль:",
                                        font=("Arial", self.ui.font_sizes['label']), bg="#ECF0F1",
                                        justify=tk.LEFT, wraplength=330,
                                        anchor=tk.W)
        self.ui.status_label.pack(pady=10, padx=5)

        # Корабли для размещения
        self.ui.ships_to_place = [
            {"size": 4, "count": 1, "placed": 0, "name": "4-палубный (1 шт)"},
            {"size": 3, "count": 2, "placed": 0, "name": "3-палубный (2 шт)"},
            {"size": 2, "count": 3, "placed": 0, "name": "2-палубный (3 шт)"},
            {"size": 1, "count": 4, "placed": 0, "name": "1-палубный (4 шт)"}
        ]

        ships_frame = tk.LabelFrame(right_column, text="КОРАБЛИ ДЛЯ РАЗМЕЩЕНИЯ",
                                    font=("Arial", self.ui.font_sizes['label'], "bold"), bg="#ECF0F1")
        ships_frame.pack(fill=tk.X, pady=5)

        for ship_info in self.ui.ships_to_place:
            ship_btn = tk.Button(ships_frame, text=ship_info["name"],
                                 command=lambda s=ship_info["size"]: self.ui.select_ship(s),
                                 font=("Arial", self.ui.font_sizes['small']),
                                 bg="#3498DB", fg="white",
                                 width=25, height=1)
            ship_btn.pack(pady=3, padx=5)
            ship_info["button"] = ship_btn

        # Кнопки управления
        control_frame = tk.LabelFrame(right_column, text="УПРАВЛЕНИЕ",
                                      font=("Arial", self.ui.font_sizes['label'], "bold"), bg="#ECF0F1")
        control_frame.pack(fill=tk.X, pady=5)

        rotate_btn = tk.Button(control_frame, text="ПОВЕРНУТЬ КОРАБЛЬ",
                               command=self.ui.rotate_ship,
                               font=("Arial", self.ui.font_sizes['small']),
                               bg="#16A085", fg="white",
                               width=25, height=1)
        rotate_btn.pack(pady=3)

        auto_btn = tk.Button(control_frame, text="АВТОРАССТАНОВКА",
                             command=self.ui.auto_place_ships,
                             font=("Arial", self.ui.font_sizes['small']),
                             bg="#27AE60", fg="white",
                             width=25, height=1)
        auto_btn.pack(pady=3)

        clear_btn = tk.Button(control_frame, text="ОЧИСТИТЬ ПОЛЕ",
                              command=self.ui.clear_ships,
                              font=("Arial", self.ui.font_sizes['small']),
                              bg="#E74C3C", fg="white",
                              width=25, height=1)
        clear_btn.pack(pady=3)

        # Кнопка начала игры
        start_battle_frame = tk.Frame(right_column, bg="#ECF0F1", height=70)
        start_battle_frame.pack(fill=tk.X, pady=10)
        start_battle_frame.pack_propagate(False)

        self.ui.start_game_btn = tk.Button(start_battle_frame, text="НАЧАТЬ БИТВУ",
                                           command=self.ui.start_battle,
                                           font=("Arial", self.ui.font_sizes['button'], "bold"),
                                           bg="#2C3E50", fg="white",
                                           state=tk.DISABLED,
                                           width=25, height=2)
        self.ui.start_game_btn.pack(pady=10)

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
                                  font=("Arial", self.ui.font_sizes['small']),
                                  bg="#ECF0F1", anchor=tk.W)
            desc_label.pack(side=tk.LEFT, padx=5)