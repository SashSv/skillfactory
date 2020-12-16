from django.db import models

# Create your models here.

# class Category(models.Model):
#     name = models.CharField(max_length= 30, unique= True, verbose_name='Название')
#     description = models.TextField(null = True, blank=True, help_text='', verbose_name='Описание')
#
#
#     # коррекция имени в админке
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'
#
# class Good(models.Model):
#     name = models.CharField()
#     category = models.ForeignKey(Category, null = True, blank = True, on_delete = CASCADE or models.SET_NULL)
#     price = models.PositiveSmallIntegerField
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Товар'
#         verbose_name_plural = 'Товары'
#         ordering = ['-price']
#
#
# class Course(models.Model):
#     name = models.CharField()
#
#     def __str__(self):
#         return self.name
#
# class Student(models.Model):
#     name = models.CharField()
#     course = models.ManyToManyField(Course)
#
#     def __str__(self):
#         return self.name