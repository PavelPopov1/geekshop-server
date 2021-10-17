from django.conf import settings
from django.db import models

# Create your models here.
from products.models import Products


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлено в обработку'),
        (PAID, 'оплачено'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдачи'),
        (CANCEL, 'отмена зазака')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус', max_length=3, default=FORMING, choices=ORDER_STATUS_CHOICES)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    @staticmethod
    def get_item(pk):
        return Order.objects.get(pk=pk)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='продукты',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество',default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'Текущий заказ {self.pk}'