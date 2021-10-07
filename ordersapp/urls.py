
from django.contrib import admin
from django.urls import path
from .views import (
    OrderList,
    OrderCreate,
    OrderRead,
    OrderUpdate,
    OrderDelete,
    forming_complete
    # order_forming_complete,
    # get_product_price,
)

app_name = 'ordersapp'

# from .ordersapp import

urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('forming/complete/<int:pk>', forming_complete, name='forming_complete'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('read/<int:pk>', OrderRead.as_view(), name='read'),
    path('update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path('delete/<int:pk>', OrderDelete.as_view(), name='delete'),

]