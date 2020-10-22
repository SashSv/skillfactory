from classClient import Client, Database

# Написать полноценную программу, которая будет все это обрабатывать и возращать результат
# База данных: 1. Юзать уже созданную 2. Создать новую базу 3. Сохранить базу
# Функционал: 1. Создать юзера 2. Посмотреть инфо юзера 3. Поменять любой параметр юзера 3. Редактировать сущ. юзера


class Employee(Client):
    def __init__(self, name='', city='', status=''):
        self.name = name
        self.city = city
        self.status = status
        
    def init_from_dict(self, employee_dict):
        self.name = employee_dict.get('name')
        self.city = employee_dict.get('city')
        self.status = employee_dict.get('status')

    def get_city(self):
        return self.city

    def change_city(self, city):
        self.city = city


    def get_status(self):
        return self.status

    def change_status(self, status):
        self.status = status


class EmplDatabase(Database):
# Методы, которые останутся без изменений
    # def __init__(self):
    # def add_db(self, db):
    # def get_db_item(self, index):
    # def change_db_item(self, index, data):
    # def get_db(self):

# Метод, который меняем
    def add_db_item(self, name = '', city = '', status= ''):
        if name and city and status:
            self.db.append({'name': name, 'city': city, 'status': status})

# Методы, которые добавляем
    def del_db_item(self, index):
        if isinstance(index, int) and 0 <= index < len(self.db):
            del self.db[index]

    def show_db_items(self):
        for index, value in enumerate(self.db):
            # print(index)
            print(f'[{index}]: {value["name"]}, {value["city"]}, {value["status"]}')


employee_list = [
    {
        "name": 'Иван Петров',
        "city": 'Москва',
        "status": "Учитель"
    },
    {
        "name": "Никита Соболев",
        "city": 'Тула',
        "status": "Наставник"
    },
    {
        "name": "Иван Иваныч",
        "city": 'Санкт-Петербург',
        "status": "Методист"
    },
]

database = EmplDatabase()
database.add_db(employee_list)
database.show_db_items()