from django.urls import path

from basket.views import basket_add, basket_del

app_name = 'basket'

urlpatterns = [
    path('basket_add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket_del/<int:id>/', basket_del, name='basket_del')
]
