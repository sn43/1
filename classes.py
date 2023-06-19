from exceptions import ShipPlacementError, ShotError
from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Для сравнения объектов класса Dot
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:
    def __init__(self, bow, lv, position):
        self.bow = bow
        self.lv = lv
        self.position = position
        self.lives = lv

    @property
    def dots(self):
        ship_dots = []
        # Получаем все точки корабля и помещаем их в список
        for i in range(self.lv):
            current_x = self.bow.x
            current_y = self.bow.y
            if self.position == 0:
                current_x += i
            elif self.position == 1:
                current_y += i
            ship_dots.append(Dot(current_x, current_y))
        return ship_dots

    def check_shot(self, shot):
        """ Проверка попадания """
        # Координаты выстрела передаются other в Dot.__eq__
        return shot in self.dots


class Board:
    def __init__(self, hide=False, size=6):
        # hide скрывает поле
        self.hide = hide
        self.size = size

        self.count = 0

        self.field = [['O'] * size for _ in range(size)]
        # busy - список занятых точек, ships - список своих кораблей
        self.busy = []
        self.ships = []

    def __str__(self):
        res = ''
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | ' + ' | '.join(row) + ' | '

        if self.hide:
            res = res.replace('■', 'O')
        return res

    def out(self, d):
        """ Точка за границей поля """
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        """ Отрисовка контура вокруг корабля """
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots:
            for dx, dy in near:
                # Берем каждую точку корабля и проходимся по near, сдвигая исходную точку на dx и dy
                current = Dot(dot.x + dx, dot.y + dy)
                if not (self.out(current)) and current not in self.busy:
                    # Если verb=True - ставим точки вокруг кораблей
                    if verb:
                        # Если точка не выходит за границы поля - помечаем и добавляем в список занятых точек
                        self.field[current.x][current.y] = '.'
                    self.busy.append(current)

    def add_ship(self, ship):
        """ Добавить корабль """
        for dot in ship.dots:
            if self.out(dot):
                raise ShipPlacementError('Корабль вышел за границы поля')
            if dot in self.busy:
                raise ShipPlacementError('Нет свободной клетки между кораблями')
        for dot in ship.dots:
            # Заменим все точки, занятые кораблем на "■" и добавим в список занятых точек
            self.field[dot.x][dot.y] = '■'
            self.busy.append(dot)
        # Добавляем корабль в список собственных кораблей и обводим по контуру
        self.ships.append(ship)
        self.contour(ship)

    def shot(self, bullet):
        """ Реализация выстрела """
        if self.out(bullet):
            raise ShotError('Выстрел за пределы поля')
        if bullet in self.busy:
            raise ShotError('Выстрел в клетку, в которую вы стреляли ранее')
        # Добавляем точку, в которую стреляли в список занятых
        self.busy.append(bullet)

        for ship in self.ships:
            # При попадании в корабль уменьшаем здоровье и помечаем точку "Х"
            if ship.check_shot(bullet):
                ship.lives -= 1
                self.field[bullet.x][bullet.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль уничтожен.')
                    # Прекращение хода
                    return False
                else:
                    print('Корабль подбит.')
                    # Повторение хода
                    return True
        # При промахе отмечаем точку
        self.field[bullet.x][bullet.y] = '.'
        print('Промах!')
        return False

    def begin(self):
        """ Обнуляет список занятых точек после расстановки кораблей """
        self.busy = []

    def defeat(self):
        """ Для проверки победителя """
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        """ Метод запроса координат от игрока """
        # Этот метод должен быть, он для наследников
        raise NotImplementedError()

    def move(self):
        """ Сделать ход """
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except ShotError as exc:
                print(exc)


class AI(Player):
    def ask(self):
        # Импортируем randint
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input('Ваш ход:').split()
            if len(cords) != 2:
                print('Введите 2 координаты:')
                continue

            x, y = cords

            # if isinstance(x, int) or (y, int):
            if not (x.isdigit()) or not (y.isdigit()):
                print()
                continue

            x, y = int(x), int(y)
            # Не забываем про индексацию
            return Dot(x - 1, y - 1)
