from classCat import Cat

cat_list = [
    {
     "name": 'Барон',
     "gender": "мальчик",
     "age": 2,
    },
    {
     "name": "Сэм",
     "gender": "Мальчик",
     "age": 2,
    }
]


for cat_item in cat_list:
    cat_obj = Cat()
    cat_obj.init_dict(cat_item)
    print(f'Имя котика - {cat_obj.getName()}. Пол котика - {cat_obj.getGender()}. Возраст котика - {cat_obj.getAge()} лет.')


