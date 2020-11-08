import random

# класс игрового корабля.
class Ship:

    def __init__(self, x, y, decks, degree = 1):
        self.x = x
        self.y = y
        self.decks = decks
        self.life = decks
        self.degree = degree
        self.is_dead = False


    def get_status(self):
        return self.is_dead

    def shot(self):
        self.life -= 1
        if self.life == 0:
            self.is_dead = True
        return True

    @property
    def positions(self):
        self.cells = []
        if self.degree:
            for i in range(self.decks):
                self.cells.append((self.x+i, self.y))
        else:
            for i in range(self.decks):
                self.cells.append((self.x, self.y+i))
        return self.cells


# Игровая доска. Для игры их создается две: под компьютер и под игрока.
class Board:

    def __init__(self, name):
        self.board = [[i for i in range(1,7)]] + [[0 for i in range(6)] for i in range(6)]
        self.name = name
        self.all_ships = []
        self.shots = None
        self.forbid_turns = []
        self.problem = []


    # метод проверки есть ли еще живые корабли - если нет, то у нас есть победитель
    def get_winner(self):
        for ship in self.all_ships:
            if not ship.get_status():
                print('\nВ море еще остались враги! Покажем им в следующем раунде!\n***********\n\n')
                return False
        print(f'\n{self.name} побеждает в этом раунде! Поздравляю!\n***********\n\n')
        return True


    # метод вывода текущего состояния доски для игры
    def print_board(self):
        for index, line in enumerate(self.board):
            line = list(map(str, line))
            print(index, ' '.join(line))


    # метод для показа текущего расположения кораблей и выстрелов - для тестирования
    # данный метод планировалось использовать вместо show_ships, однако этот метод меняет аттрибут self.board
    # на момент сдачи работы решить из-за чего возникает проблема не удалось
    def show_ships_test(self):
        new_board = self.board.copy()
        for ship in self.all_ships:
            for position in ship.positions:
                x, y = position
                if new_board[x][y] != 'x' and new_board[x][y] != '■':
                    new_board[x][y] = '■'
        for index, line in enumerate(new_board):
            line = list(map(str, line))
            print(index, ' '.join(line))


    # метод для показа текущего расположения кораблей игроку, чтобы было понимание куда можно размещать, а куда нет
    # изначально планировалось использовать для этой цели show_ships_test(self)
    def show_ships(self):
        new_board = [[i for i in range(1,7)]] + [[0 for i in range(6)] for i in range(6)]
        for ship in self.all_ships:
            for position in ship.positions:
                x, y = position
                new_board[x][y] = '■'
        for index, line in enumerate(new_board):
            line = list(map(str, line))
            print(index, ' '.join(line))


    # метод для проверки на возможность разместить корабль в данной точке
    def check_empty(self, cell):
        if self.all_ships is None:
            return True
        else:
            for ship in self.all_ships:
                if cell in ship.positions:
                    return False
                else:
                    if cell in self.forbid_turns:
                        return False
            return True


    # метод проверки что координата находится в рамках игрового поля
    def check_in_field(self, cell):
        x,y = cell
        if x in range(1,len(self.board)) and y in range(0,len(self.board[0])):
            return True
        else:
            return False


    # метод генераниции клеток в которые запрещено ставить корабли
    # берет клетку создаваемого коробля и в пишет в запретные клетки все клетки вокруг нее в радиусе 1
    def gener_forbid_turns(self, cell):
       x,y = cell
       for row in range(-1, 2):
            for col in range(-1, 2):
                if x + row > 0 and y + col >= 0:
                    if (x + row, y + col) not in self.forbid_turns \
                            and (x + row, y + col) != (x,y):
                        self.forbid_turns.append((x + row, y + col))


    # метод размещения кораблей на полей
    def set_ship(self,*args):
        new_ship = Ship(*args)
        go = []
        for cell in new_ship.positions:
            # проверяем, чтобы каждая клетка была свободна от другого корабля, клетка не находилась в списке
            # запретных клеток (правило - миниму 1 клетка от соседнего корабля), а также клетка корабля должна
            # находится в рамках текущего игрового поля
            result = self.check_empty(cell) and self.check_in_field(cell)
            go.append(result)

        if all(go):
            if self.all_ships is None:
                self.all_ships = []
            self.all_ships.append(new_ship)
            for i, cell in enumerate(new_ship.positions):
                self.gener_forbid_turns(cell)
            return True
        else:
            return False


    # метод выделения подбитого корабля. Если корабль уничтожен, то все клетки в радиусе 1 меняют внешний вид
    # для обозначения контура подбитого корабля и знак игроку, что стрелять туда не имеет смысла
    def ship_dead(self, positions):
        for cell in positions:
            x,y = cell
            for row in range(-1, 2):
                for col in range(-1, 2):
                    if x + row in range(1, len(self.board)) and y + col in range(0,len(self.board[0]))\
                    and ((x + row, y + col) != cell and self.board[x + row][y + col] != 'x' and self.board[x + row][y + col] != '■'):
                        self.board[x + row][y + col] = '•'


    # метод общения игрока с программой - фактически просит ввести координаты и проверяет ввод является числами
    # и эти числа находятся в рамках игрового поля
    def user_choice(self):
        text = f'Ваши координаты должны быть целыми числами от 1 до {len(self.board[0])}.'
        while True:
            x = input ('\nВыберите ряд - ')
            try:
                x = int(x)
                if x not in range(1,len(self.board)):
                    print(text)
                else:
                    break
            except ValueError:
                print(text)
        while True:
            y = input('Выберите колонку - ')
            try:
                y = int(y) - 1
                if y < 0 or y > len(self.board[0]):
                    print(text)
                else:
                    break
            except ValueError:
                print(text)
        return x,y


    # метод - выстрел человека
    def shot_user(self):
        while True:
            print(f'{self.name} приготовиться к атаке! Вывожу последние данные:')
            self.print_board()
            x,y = self.user_choice()
            go = self.shot(x,y)
            if go:
                break
            print('Ой! Мы уже стреляли в эту клетку! Надо выбрать другую.\n')


    # обработка выстрела - получаем координаты от игрока или компьютера и обрабатываем их
    def shot(self, x, y):
        x,y = x,y
        if self.shots is None:
            self.shots = []
        if (x, y) in self.shots:
            return False
        for ship in self.all_ships:
            if (x, y) in ship.positions:
                print('Попадание! Так держать коммандор!\n')
                self.board[x][y] = 'x'
                ship.shot()
                if ship.get_status():
                    self.ship_dead(ship.positions)
                    print('Корабль врага повержен!\n')
                self.shots.append((x, y))
                return True
        print('Мимо! В следующий раз точно повезет!\n')
        self.board[x][y] = '•'
        self.shots.append((x, y))
        return True


    # метод - выстрел компьютера
    def shot_ai(self):
        while True:
            x,y = (random.randint(1, 6),random.randint(0, 5))
            if self.shots is None:
                self.shots = []
            if (x,y) not in self.shots:
                break
        print(f'{self.name} выбирает для выстрела клетку - {x},{y + 1}!')
        self.shot(x,y)


    # метод-генерация доски игроком
    def set_user_deck(self):
        decks = (1,1,1,3,)
        for i, deck in enumerate(decks):
            while True:
                print(f'Размещаем корабль {i + 1}. Количество палуб - {deck}.')
                self.show_ships()
                degree = 1
                if deck > 1:
                    while True:
                        degree = input('''Это большой корабль! Выберите положение для корабля:
1 - следующие палубы пойдут от стартовой координаты вниз.
0 - следующие палубы пойдут от стартовой координаты вправо.
Вы выбираете - ''')
                        try:
                            degree = int(degree)
                            if degree in range(0,2):
                                break
                            else:
                                print('Ошибка! Вы должны напечатать 1 или 0. Попробуйте снова.')
                        except ValueError:
                            print('Ошибка! Вы должны напечатать 1 или 0. Попробуйте снова.')
                x,y = self.user_choice()
                if self.set_ship(x, y, deck, degree):
                    print('Отлично! Корабль размещен!\n')
                    break
                else:
                    print('Командор! У нас ошибка: эта зона занята другим кораблем. Попробуем разместить заново.')
        print('Отлично! Все корабли на месте. Начинаем игру.')


    # метод-генерация доски компьютером
    def set_ai_deck(self):
        decks = (1,1,1,3,)
        for deck in decks:
            while True:
                x,y = random.randint(1,6), random.randint(0,5)
                degree = random.randint(0,1)
                go = self.set_ship(x,y,deck,degree)
                if go:
                    break


# данный класс отвечает за запуск игры, и режимы игры: игра между ИИ (для поиска проблем), игра между компьютером
# человеком. По идее используя данный контроллер и класс Board можно еще написать вариант игры между 2 игроками
class GameContoller:
    def __init__(self):
        self.comp_1 = 'Comp 1'
        self.comp_2 = 'Comp 2'

    # рандомайзер хода для теста Комп против компа
    def who_is_first_ai(self, deck_1, deck_2):
        print(f'Определяем кто начинает партию: {deck_1.username} или {deck_2.username}.')
        turn = random.randint(0,1)
        if turn:
            print(f'Первым ходит {deck_1.username}')
            return deck_1, deck_2
        print(f'Первым ходит {deck_2.username}')
        return deck_2, deck_1

    # создаем имя игрока для типа игры Комп vs Игрок
    def set_user(self):
        self.user = input('Добро пожаловать в игру!\nНазовите свое имя: ')

    # тестирование игры на компьютерах
    def ai_game(self):
        board_1, board_2 = Board(self.comp_1), Board(self.comp_2)
        print(f'Добро пожаловать в игру - {board_1.username}, {board_2.username} ')
        board_1, board_2 = self.who_is_first_ai(board_1, board_2)
        print('Резмещаем свои корабли!')
        board_1.set_ai_deck()
        board_2.set_ai_deck()
        while True:
            print(f'Ход игрока {board_1.username}')
            board_1.print_board()
            print()
            board_1.shot_ai()
            board_1.print_board()
            game_over = input('Едем дальше? - ')
            if game_over:
                break
            game_over = board_1.get_winner()
            if game_over:
                break
            board_1, board_2 = board_2, board_1

    # метод для запуска игры между компьютером или человеком
    # он получился немного перегруженный - не успел нормально переписать
    def game(self):
        self.set_user()
        userBoard, aiBoard = Board(self.user), Board(self.comp_1)
        userBoard.set_ai_deck()
        aiBoard.set_user_deck()
        user_start = random.randint(0,1)

        print('\nВеликий рандом решил, что человек будет ходить первым!') if user_start else print('\nВеликий рандом решил, что компьютер будет ходить первым!')
        while True:
            if user_start:
                userBoard.shot_user()
                print('Вывожу результат:')
                userBoard.print_board()
                if userBoard.get_winner():
                    break

                aiBoard.shot_ai()
                print('Вывожу результат:')
                aiBoard.print_board()
                if aiBoard.get_winner():
                    break
            else:
                aiBoard.shot_ai()
                print('Вывожу результат:')
                aiBoard.print_board()
                if aiBoard.get_winner():
                    break
                userBoard.shot_user()
                print('Вывожу результат:')
                userBoard.print_board()
                if userBoard.get_winner():
                    break

game = GameContoller()
game.game()