from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, unique = True)
    author_raiting = models.IntegerField(default = 0)

    def update_raiting(self):
        posts = Post.objects.filter(author=self.id) # все посты автора
        post_raiting = sum([r.post_raiting * 3 for r in posts]) # рейтинг каждого поста автора умножен на 3
        comment_raiting = sum([r.comment_raiting for r in Comment.objects.filter(author=self.author)]) # сумма лайков/дислайков к комментам автора
        all_to_post_comment_raiting = sum([r.comment_raiting for r in Comment.objects.filter(post__in = posts)]) # сумма лайков/дислайков всех комментов к постам автора
        self.author_raiting = post_raiting + comment_raiting + all_to_post_comment_raiting
        self.save()

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'

    POST_TYPES = [
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    ]
    type = models.CharField(max_length=2, choices = POST_TYPES, default = NEWS)
    created_time = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, related_name='posts', blank=True)
    header = models.CharField(max_length = 255)
    article_text = models.TextField()
    post_raiting = models.IntegerField(default = 0)

    @property
    def short_header(self):
        if len(self.header) > 50:
            return self.header[:50]+'...'
        else:
            return self.header



    def post_delete_url(self):
        return reverse('post_delete_url', kwargs={'pk': self.pk})

    def post_update_url(self):
        return reverse('post_update_url', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


    def preview(self):
        preview = self.article_text[:129] + '...'
        return preview

    def like(self):
        self.post_raiting += 1
        self.save()

    def dislike(self):
        self.post_raiting -= 1
        self.save()

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'



# class PostCategory(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#
#     def __str__(self):
#         result = f'{self.category.name} - {self.post.header[:15]}'
#         return result
#
#     class Meta:
#         db_table = 'blogapp_post_category'
#         verbose_name = 'ПостКатегория'
#         verbose_name_plural = 'ПостКатегории'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    comment_raiting = models.IntegerField(default = 0)

    def like(self):
        self.comment_raiting += 1
        self.save()

    def dislike(self):
        self.comment_raiting -= 1
        self.save()

    def __str__(self):
        result = f'{self.author.username} - {self.post.header} - {self.created_time.strftime("%d, %b %Y - %H:%M")}'
        return result

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'