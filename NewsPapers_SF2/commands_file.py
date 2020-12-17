#  Создаем пользователей
User.objects.create(username='Jack Jack', password='12345')
User.objects.create(username='Tom Cruz', password='12345')

# Создаем авторов (в модели уже пользователи поэтому id 5 и 6)
Author.objects.create(author=User.objects.get(id=5))
Author.objects.create(author=User.objects.get(id=6))

# Создаем категории
Category.objects.create(name='Спорт')
Category.objects.create(name='Путешествия')
Category.objects.create(name='Бизнес')
Category.objects.create(name='Технологии')

# Создаем новости и статьи
# Повторить в зависимости от желаемого количества новостей
Post.objects.create(author=Author.objects.get(id=5), type = 'NW',
                    header= 'Еще одна интересная новость',
                    article_text='Прикольный текст, который используется в новости')

# Присваиваем категории новости из примера выше id=5
# Вар 1
post = Post.objects.get(id=5)
post.category.add(Category.objects.get(id=1))

# Вар 2
cat = Category.objects.get(id=2)
PostCategory.objects.create(post=post, category = cat)

# Создаем комментарии
author = User.objects.get(id=6)
post = Post.objects.get(id=5)
Comment.objects.create(post=post, author=author, text='Здесь будет текст комментария')

# Ставим лайки комментариям
comments = Comment.objects.all()
comments[6].like() # 3 лайка для Тома Круза

# Ставим лайки для поста
post.like()

# меняем рейтинг посту
post.post_raiting = 100
post.save()

# Обновляем рейтинги авторов
for auth in Author.objects.all():
    auth.update_raiting()

# Вывести имя и рейтинг лучшего пользоветеля
Author.objects.all().order_by('-author_raiting').values('author__username','author_raiting')[0]

# Вывести самую крутую статью
best = Post.objects.all().order_by('-post_raiting')[0]
best_post= Post.objects.all().order_by('-post_raiting').values( # выводим параметры
    'created_time',
    'author__author__username',
    'header', 'post_raiting',
    'article_text')[0]
best.preview()

# Вывести все комменты к статье
Comment.objects.filter(post=best).values('author__username', 'created_time', 'text')