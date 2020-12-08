from django.db import models
from datetime import datetime


# one_to_one_relation = models.OneToOneField(some_model)
# one_to_many_relation = models.ForeignKey(some_model)
# many_to_many_relation = models.ManyToManyField(some_model)

# python manage.py makemigrations
# python manage.py migrate
# python manage.py shell
# from rest.models import Product


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)



director = "DI"
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
    labor_contact = models.IntegerField(default=0)

    def get_lastname(self):
        return self.full_name.split()[0]


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    coast = models.FloatField(default=0)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete = models.CASCADE)

    products = models.ManyToManyField(Product, through = 'ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        before = self.time_in
        if self.complete:
            after = self.time_out
        else:
            after = datetime.now()

        return (after - before).total_seconds() // 60



class ProductOrder(models.Model):

    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    order = models.ForeignKey(Order, on_delete = models.CASCADE)

    _amount = models.IntegerField(default=1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()


    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount


potatoe_small = Product.objects.create(name='Картофель фри (станд.)',price=83.0)
potatoe_small.save()
potatoe_big = Product.objects.create(name='Картофель фри (бол.)',price=106.0)