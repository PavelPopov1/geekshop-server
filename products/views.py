from django.conf import settings
from django.views.generic.list import ListView

from products.models import Products, ProductCategory, NewProducts
from django.views.decorators.cache import cache_page, never_cache
from django.shortcuts import render, get_object_or_404
from django.core.cache import cache


def get_links_category():
    if settings.LOW_CACHE:
        key = 'links_category'
        links_category = cache.get(key)

        if links_category is None:
            links_category = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_category)
        return links_category
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)

        if product is None:
            product = get_object_or_404(Products, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Products, pk=pk)


def get_links_product():
    if settings.LOW_CACHE:
        key = 'links_product'
        links_product = cache.get(key)

        if links_product is None:
            links_product = Products.objects.filter(is_active=True).select_related()
            cache.set(key, links_product)
        return links_product
    else:
        return Products.objects.filter(is_active=True).select_related()


def view_random_hot_product():
    rand_obj = NewProducts.objects.order_by('?')[0]
    if rand_obj.id:
        view_product = rand_obj.product_key
    else:
        return
    return view_product

# Create your views here.


class IndexView(ListView):
    model = Products
    template_name = 'products/index.html'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = 'Магазин'
        context['icon'] = 'img/icon_add.png'
        context['socials'] = ["social1",
                              "social2",
                              "social3",
                              "social4"]
        context['media_path'] = settings.MEDIA_URL
        return context


class ProductsListView(ListView):
    template_name = 'products/products.html'
    model = Products
    paginate_by = 2

    def get_queryset(self):
        if self.kwargs.get('category_type_id'):
            return Products.objects.filter(category_type_id=self.kwargs.get('category_type_id')).order_by('id').select_related('category')
        else:
            return Products.objects.all().order_by('id').select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог товаров'
        context['icon'] = 'img/icon-hover.png'
        context['controls'] = ["social1",
                               "social2",
                               "social3",
                               "social4"]
        context['media_path'] = settings.MEDIA_URL
        context['categories'] = get_links_category()
        context['hot_product'] = view_random_hot_product()
        if self.kwargs.get('category_type_id'):
            context['category_type_id'] = self.kwargs.get('category_type_id')
        return context








