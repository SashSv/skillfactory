import random

def print_field(field):
    field = list(map(str, field))
    for i in range(0,len(field), 3):
        print(" | ".join(field[i:i+3]))
        if i < 6:
            print("– | – | –")

def checking_win(field, mark):
    turns_of_current_mark = [i for i, d in enumerate(field) if d == mark] # все ходы игрока mark
    combos_to_win = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8)]
    # print("*** Проверка ***")
    # print(f'Текущий знак - {mark}. Комбо для знака - {turns_of_current_mark}')

    for combo in combos_to_win: # проверяем есть ли одно из выиграшных комбо в текущем наборе ходов игрока
        check = all(item in turns_of_current_mark for item in combo)
        if check:
            print(f'Игрок со знаком {mark} - победил!')
            return True

    check = any(isinstance(i, int) for i in field)  # проверяем остались ли пустые клетки в принципе
    if not check:
        print('Ничья!')
        return True
    return False


def player(field, mark):
    print('Ход игрока!')
    while True:
        turn = int(input('Выберите клетку!\n')) # Добавить обработку ошибок на случай ввода буквы или float
        if turn in field:
            field[turn - 1] = mark
            print_field(field)
            if checking_win(field, mark):
                return field, False # поле и игра закончилась
            return field, True # поле и игра продолжается
        else:
            print(f'Клетка {turn} занята либо отсуствует. Попробуйте снова.')

def computer(field, mark):
    print('Ход компьютера!')
    while True:
        turn = random.randint(1, 9)
        if turn in field:
            print(f'Компьютер выбрал клетку {turn}!')
            field[turn - 1] = mark
            if checking_win(field, mark):
                return field, False # поле и игра закончилась
            print_field(field)
            return field, True # поле и игра продолжается

def game():
    print("Определяем кто ходит первым!")
    whoStart = random.randint(0, 1)
    # print(whoStart)
    field = [i for i in range(1, 10)]
    go = True
    # надо как-то переработать эту часть - start
    if whoStart:
        print("Игрок ходит первым!")
        print_field(field)
        while go:
            field, go = player(field, "X")
            if not go:
                break
            field, go = computer(field, "O")
    else:
        print("Компьютер ходит первым!")
        print_field(field)
        while go:
            field, go = computer(field, "X")
            if not go:
                break
            field, go = player(field, "O")
    # надо как-то переработать эту часть - stop

    newGame = input('Играем снова?')
    if newGame:
        game()
game()