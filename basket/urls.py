from django.urls import path

from basket.views import basket_add, basket_del, basket_edit

app_name = 'basket'

urlpatterns = [
    path('basket_add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket_del/<int:id>/', basket_del, name='basket_del'),
    path('basket_edit/<int:id>/<int:quantity>/', basket_edit, name='basket_edit')
]
