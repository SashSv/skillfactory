# создан класс для клиента
class Client:
    def __init__(self, name='', balance=0):
        self.name = name
        self.balance = balance

    def init_from_dict(self, client_dict):
        self.name = client_dict.get('name')
        self.balance = client_dict.get('balance')

    def get_name(self):
        return self.name

    def get_balance(self):
        return self.balance

    def change_name(self, name):
        self.name = name

    def change_balance(self, balance):
        self.balance = balance

    def get_client(self):
        return {'name': self.name, 'balance': self.balance}

# создан класс для базы данных: она будет принимать список клиентов и изменять список клиентов
class Database:
    def __init__(self):
        self.db = []

    def add_db(self, db):
        self.db = db.copy() # тут делаем копию иначе изменения будут вноситься в оригинальный список

    def add_db_item(self, name, value):
        self.db.append({'name': name, 'balance': value})

    def get_db_item(self, index):
        if isinstance(index, int) and 0 <= index < len(self.db):
            # print(self.db[index])
            return self.db[index]
        else:
            print('Вы ввели неправильный индекс.')

    def change_db_item(self, index, data):
        if isinstance(index, int) and 0 <= index < len(self.db):
            self.db[index] = data
        else:
            print('Вы ввели неправильный индекс.')


    def get_db(self):
        return self.db

# создаю класс наследник, который будет работать со списком объектов,
# а не словарей
class Database2(Database):
    # методы, которые наследуются без изменений
    # __init__, add_db, get_db_item,

    # Методы, которые меняются
    def add_db_item(self, name = "", value = 0):
        customer = Client(name, value)
        self.db.append(customer)

    # Посмотреть инфо о выбранном объекте в человеческом виде
    def get_item_stats(self, index):
        if isinstance(index, int) and 0 <= index < len(self.db):
            print(self.db[index].get_client())

    # Создание базы с объектами Client на основе списка
    def create_db_from(self, lst):
        self.db = []
        customer = Client()
        for i in lst:
            customer.init_from_dict(i)
            print(i)
            self.db.append(customer)


# тут как бы происходит импорт данных о покупателях откуда-то
client_list = [
    {
     "name": 'Иван Петров',
     "balance": 500,
    },
    {
     "name": "Никита Соболев",
     "balance": 122,
    },
    {
     "name": "Иван Иваныч",
     "balance": 100,
    },
]

database = Database2()
database.create_db_from(client_list)
database.add_db_item('Федор Иванович', 100)
database.get_item_stats(3)