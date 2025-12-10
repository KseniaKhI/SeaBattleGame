#!/usr/bin/env python3
"""
Главный файл запуска игры Морской бой
"""

from ui.game_ui import SeaBattleGame


def main():
    """Запуск игры"""
    try:
        game = SeaBattleGame()
        game.run()
    except Exception as e:
        print(f"Ошибка при запуске игры: {e}")
        input("Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()