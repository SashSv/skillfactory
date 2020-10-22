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