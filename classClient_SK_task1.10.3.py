# создан класс для клиента
class Client:
    def __init__(self, name='', balance=0):
        self.name = name
        self.balance = 0

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

# ниже идет код чисто для тестирования функционала на миниальную работоспособность

database = Database() # создаем экземпляр базы
database.add_db(client_list) # загружаем старый список клиентов

customer = Client() # создаем экземпляр клиента
customer.init_from_dict(database.get_db_item(0)) # загружаем туда клиента из базы для работы с ним

print(f'Клиент «{customer.get_name()}». Баланс: {customer.get_balance()} руб.')

customer.change_name('Игорь') # меняем имя клиента
customer.change_balance(100) # меняем баланс клиента

print(f'Клиент «{customer.get_name()}». Баланс: {customer.get_balance()} руб.')

database.change_db_item(0, customer.get_client()) # загружаем изменения в базу
database.get_db_item(0) # изменения появились в базе

client_list_2 = database.get_db() # получили на выход обновленный список - можем отправить откуда он пришел к нам

# и проверка что на входе и выходе лежат разные штуки
print(client_list is client_list_2)

