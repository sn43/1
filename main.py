from exceptions import ShipPlacementError, ShotError
from classes import *


class Game:
    def try_board(self):
        """ Попытка генерации доски с кораблями """
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attemps = 0
        for l in lens:
            # Попытка поставить корабль для каждой длины корабля, начиная с большего
            while True:
                attemps += 1
                if attemps > 3000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    # Корабль поставлен
                    break
                except ShipPlacementError:
                    # Следующая попытка
                    pass

        board.begin()
        return board

    def random_board(self):
        """ Создать доску """
        board = None
        while board is None:
            # Будет повторять итерацию, пока доска пустая
            board = self.try_board()
        return board

    def __init__(self, size=6):
        """ Создаем два поля """
        self.size = size
        user = self.random_board()
        ai = self.random_board()
        ai.hide = True
        # Создаем игроков
        self.ai = AI(ai, user)
        self.us = User(user, ai)

    def greet(self):
        print('-------------------')
        print(' Приветствуем вас  ')
        print('      в игре       ')
        print('    морской бой    ')
        print('-------------------')
        print('   Формат ввода:   ')
        print('   координаты х у  ')
        print(' х - номер строки  ')
        print(' у - номер столбца ')
        print('-------------------')

    def loop(self):
        """ Игровой цикл """
        # Номер хода. Четный - игрок, нечетный - компьютер
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
                # При повторе хода значение в переменной num не меняется
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.defeat():
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        """ Запуск игры """
        self.greet()
        self.loop()


g = Game()
g.start()