import random
# for test
def printField(field):
    field = list(map(str, field))
    for i in range(0,len(field), 3):
        print(" | ".join(field[i:i+3]))
        if i < 6:
            print("– | – | –")

def checkWinner(field, mark):
    currentCombo = [i for i, d in enumerate(field) if d == mark] # все ходы игрока mark
    winCombos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8)]
    print("*** Проверка ***")
    print(f'Текущий знак - {mark}. Комбо для знака - {currentCombo}')

    for combo in winCombos: # проверяем есть ли одно из выиграшных комбо в текущем наборе ходов игрока
        check = all(item in currentCombo for item in combo)
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
            printField(field)
            if checkWinner(field, mark):
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
            if checkWinner(field, mark):
                return field, False # поле и игра закончилась
            printField(field)
            return field, True # поле и игра продолжается

def game():
    print("Определяем кто ходит первым!")
    whoStart = random.randint(0, 1)
    print(whoStart)
    field = [i for i in range(1, 10)]
    go = True

    if whoStart:
        print("Игрок ходит первым!")
        printField(field)
        while go:
            field, go = player(field, "X")
            if not go:
                break
            field, go = computer(field, "O")
    else:
        print("Компьютер ходит первым!")
        printField(field)
        while go:
            field, go = computer(field, "X")
            if not go:
                break
            field, go = player(field, "O")

    newGame = input('Играем снова?')
    if newGame:
        game()
game()