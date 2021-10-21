from django.urls import path

from products.views import ProductsListView
from django.views.decorators.cache import cache_page

app_name = 'products'

urlpatterns = [
    path('', cache_page(3600)(ProductsListView.as_view()), name='index'),
    # path('', ProductsListView.as_view(), name='index'),
    path('<int:category_type_id>/', ProductsListView.as_view(), name='product'),
    path('page/<int:page>/', ProductsListView.as_view(), name='page'),
    path('<int:category_type_id>/page/<int:page>/', ProductsListView.as_view(), name='filter_page')
]
