from django.db import models
from datetime import datetime

# Create your models here.



director = 'DI'
admin = 'AD'
cook = 'CO'
cashier = 'CA'
cleaner = 'CL'

POSITIONS = [
    (director, 'Директор'),
    (admin, 'Администратор'),
    (cook, 'Повар'),
    (cashier, 'Кассир'),
    (cleaner, 'Уборщик')
]


class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices = POSITIONS, default = cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]


class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default= 0.0)
    composition = models.TextField(default="Состав не указан")


class Orders(models.Model):
    time_in = models.DateTimeField(auto_now_add = True)
    time_out = models.DateTimeField(null = True)
    cost = models.FloatField(default = 0.0)
    take_away = models.BooleanField(default = False)
    complete = models.BooleanField(default = False)

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        before = self.time_in
        if not complete:
            after = datetime.now()
        else:
            after = self.time_out
        return (after - before).total_seconds() // 60


class ProductsOrders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    in_order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    _amount = models.IntegerField(default = 1, db_column = 'amount')

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()