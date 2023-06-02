cell = [1, 2, 3,
        4, 5, 6,
        7, 8, 9]

win_combinations = [[0, 1, 2],
                    [3, 4, 5],
                    [6, 7, 8],
                    [0, 3, 6],
                    [1, 4, 7],
                    [2, 5, 8],
                    [0, 4, 8],
                    [2, 4, 6]]


def print_game_board():
    """ Функция отображения игрового поля. """
    print(f' | {cell[0]} | {cell[1]} | {cell[2]} |')
    print(f' | {cell[3]} | {cell[4]} | {cell[5]} |')
    print(f' | {cell[6]} | {cell[7]} | {cell[8]} |')


def player_step(step, side):
    """ Функция реализации хода игрока. """
    idx = cell.index(step)
    cell[idx] = side


def check_winner():
    """ Функция проверки на наличие победных комбинаций. """
    winner = None
    for win in win_combinations:
        if cell[win[0]] == 'X' and cell[win[1]] == 'X' and cell[win[2]] == 'X':
            winner = 'Победил первый игрок (X)'
        if cell[win[0]] == 'O' and cell[win[1]] == 'O' and cell[win[2]] == 'O':
            winner = 'Победил второй игрок (O)'
    return winner


player_x = True
endgame = False

while endgame is False:
    """ Функция, определяющая ход игры. """
    print_game_board()
    if player_x is True:
        step = int(input('Игрок 1, введите номер клетки: '))
        side = 'X'
    else:
        step = int(input('Игрок 2, введите номер клетки: '))
        side = 'O'
    player_step(step, side)
    winner = check_winner()
    if winner is None:
        endgame = False
    else:
        endgame = True
    player_x = not player_x

print(print_game_board())
print(f' Игра окончена. {winner}')
