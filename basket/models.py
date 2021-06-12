from django.db import models

from users.models import User
from products.models import Products


# Create your models here.

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    @property
    def all_bask(self):
        return Basket.objects.filter(user=self.user)

    def total_sum(self):
        return sum([basket.sum() for basket in self.all_bask])

    def total_quantity(self):
        return sum(map(lambda x: x.quantity, self.all_bask))