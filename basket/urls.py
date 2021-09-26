from django.urls import path

from basket.views import BasketAddView, BasketDelView, basket_edit

app_name = 'basket'

urlpatterns = [
    path('basket_add/<int:product_id>/', BasketAddView.as_view(), name='basket_add'),
    path('basket_del/<int:id>/', BasketDelView.as_view(), name='basket_del'),
    path('basket_edit/<int:id>/<int:quantity>/', basket_edit, name='basket_edit')
]
